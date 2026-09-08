#!/usr/bin/env python3
"""Prova a página de pagamento num navegador de verdade (Chromium do Playwright).

    python3 testes/medir_checkout.py            # tudo simulado, três tamanhos de tela
    python3 testes/medir_checkout.py --real-sdk # baixa o SDK e a chave PÚBLICA de verdade
                                                # e mede se o Brick abre mesmo

⛔ NADA aqui toca a produção. As duas rotas do servidor (`wcp/checkout/sessao` e
   `wcp/pagamento/criar`) são interceptadas e respondidas pelo próprio teste.
   No modo padrão o SDK do Mercado Pago também é substituído por um dublê, o que
   deixa provar o CAMINHO INTEIRO (envio, Pix, recusa, aprovação) sem cartão, sem
   conta e sem rede. O que o dublê NÃO prova é o Brick de verdade abrindo: para
   isso existe o `--real-sdk`, que usa a chave pública real.

O que mede (✅/🔴 por item):
- estrutura, em 360×640, 390×844 e 1440×900: estouro horizontal, um h1 só, lang,
  noindex, imagem com alt/width/height, âncora morta, erro de JavaScript, alvo de
  toque ≥ 44 px (fora do Brick, que é desenho do Mercado Pago)
- sessão válida: o Brick é montado, o valor da tela vem do SERVIDOR e o primeiro
  nome aparece
- sessão de teste: a faixa "sessão de teste" acende e o valor é o de teste
- sessão vencida (404) e Mercado Pago desligado (503): a recusa aparece e o Brick
  NÃO é montado
- envio: o corpo do POST leva idempotência UUID v4 nova a cada envio, o token da
  sessão, o tipo, o e-mail e o device id
- aprovado → vai para obrigado.html · Pix → QR, copia e cola e botão de copiar
- recusado → motivo em português e o formulário continua na tela
- 429 → "muitas tentativas" · 502 → a falha aparece
- obrigado.html: estrutura, e a contagem de pendências da faixa bate com o DOM
- travessão no meio de frase: zero, nas duas páginas e no JavaScript

⚠️ O que este arquivo NÃO prova, e onde a prova está:
- o preflight OPTIONS do POST em JSON: o Playwright responde pela rota sem que o
  Chromium dispare o OPTIONS. Medido fora, com curl, em 08/09/2026 (204 com
  `access-control-allow-headers: content-type`).
- o Brick de verdade: só com `--real-sdk`, e ele depende da chave pública da
  config estar válida no Mercado Pago.
- capturas em testes/capturas/checkout-<tamanho>.png
"""
import argparse, functools, http.server, json, os, re, sys, threading

from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
TAMANHOS = {"360x640": (360, 640), "390x844": (390, 844), "1440x900": (1440, 900)}
TOKEN = "ab12" * 12  # 48 caracteres, o mesmo formato do encode(gen_random_bytes(24),'hex')
CHAVE_FALSA = "TEST-chave-publica-de-mentira"
UUID4 = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")

ok_n = ruim_n = 0

SESSAO_OK = {"ok": True, "valor": 97, "primeiro_nome": "Marcelo", "email": "marcelo@example.com",
             "public_key": CHAVE_FALSA, "max_parcelas": 6, "teste": False,
             "expira_em": "2026-09-10T12:00:00-03:00"}

# Dublê do SDK: implementa só o que a nossa página usa, e guarda a configuração
# recebida para o teste conferir que o tema e o valor saíram do lugar certo.
SDK_DUBLE = r"""
window.MP_DEVICE_SESSION_ID = 'device-de-teste';
window.MercadoPago = function (chave) {
  if (!chave) { throw new Error('sem chave'); }
  window.__chave = chave;
  this.bricks = function () {
    return {
      create: function (tipo, container, config) {
        return new Promise(function (resolve) {
          var alvo = document.getElementById(container);
          alvo.innerHTML = '<div class="brick-duble"><p>formulario do Mercado Pago</p></div>';
          window.__config = config;
          /* O Brick de verdade lê a promessa do onSubmit: resolvida = seguiu,
             rejeitada = fica na tela para tentar de novo. O dublê guarda esse
             veredito em __submit para o teste conferir. */
          window.__enviar = function (dados) {
            window.__submit = 'pendente';
            var p = config.callbacks.onSubmit(dados);
            if (p && p.then) { p.then(function () { window.__submit = 'seguiu'; },
                                      function () { window.__submit = 'tenta de novo'; }); }
            return true;
          };
          window.__erro = function (e) { return config.callbacks.onError(e); };
          var ctrl = { unmount: function () { alvo.innerHTML = ''; window.__desmontado = true; } };
          window.paymentBrickController = ctrl;
          setTimeout(function () { config.callbacks.onReady(); }, 20);
          resolve(ctrl);
        });
      }
    };
  };
};
"""

CORS = {"access-control-allow-origin": "*",
        "access-control-allow-headers": "content-type",
        "access-control-allow-methods": "POST, GET, OPTIONS"}


def t(rotulo, cond, extra=""):
    global ok_n, ruim_n
    cond = bool(cond)
    ok_n += cond; ruim_n += (not cond)
    print(f"{'✅' if cond else '🔴'} {rotulo}{(' · ' + str(extra)) if extra else ''}")


class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):  # o servidor local não polui a saída do teste
        pass


def sobe_servidor():
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quieto, directory=RAIZ))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


class Cenario:
    """Uma aba, com as rotas do servidor e do SDK já interceptadas."""

    def __init__(self, ctx, base, sessao=None, codigo_sessao=200, real_sdk=False):
        self.envios = []
        self.resposta_pagamento = {"status": 200, "corpo": {"ok": True, "status": "approved", "payment_id": "1"}}
        self.pg = ctx.new_page()
        self.erros_js = []
        self.pg.on("pageerror", lambda e: self.erros_js.append(str(e)))
        self.base = base

        corpo_sessao = sessao if sessao is not None else SESSAO_OK

        def rota_sessao(route, request):
            if request.method == "OPTIONS":
                return route.fulfill(status=204, headers=CORS)
            route.fulfill(status=codigo_sessao, headers=CORS, content_type="application/json",
                          body=json.dumps(corpo_sessao))

        self.preflights = []
        def rota_pagamento(route, request):
            if request.method == "OPTIONS":
                self.preflights.append(request.url)
                return route.fulfill(status=204, headers=CORS)
            self.envios.append(request.post_data or "")
            r = self.resposta_pagamento
            route.fulfill(status=r["status"], headers=CORS, content_type="application/json",
                          body=json.dumps(r["corpo"]))

        # ⛔ Rede de segurança, e ela entra PRIMEIRO de propósito: quando duas rotas
        #    casam, o Playwright usa a registrada por ÚLTIMO. Então a barra genérica
        #    vem antes e as rotas específicas, depois, passam na frente dela.
        #    Qualquer outra saída para o Mercado Pago ou para o nosso servidor é
        #    abortada: se o teste vazar para produção, ele quebra em vez de cobrar
        #    alguém de verdade.
        self.vazamentos = []
        def barra(route, request):
            self.vazamentos.append(request.url)
            route.abort()
        self.pg.route("https://api.mercadopago.com/**", barra)
        self.pg.route("https://n8n-webhook.clinixsystem.com.br/**", barra)

        if not real_sdk:
            self.pg.route("https://sdk.mercadopago.com/**",
                          lambda route, req: route.fulfill(status=200, content_type="application/javascript",
                                                           body=SDK_DUBLE))
        self.pg.route("**/webhook/wcp/checkout/sessao*", rota_sessao)
        self.pg.route("**/webhook/wcp/pagamento/criar", rota_pagamento)

    def abre(self, pagina="checkout.html", query="?c=" + TOKEN):
        self.pg.goto(self.base + "/" + pagina + query, wait_until="load")
        self.pg.wait_for_timeout(500)
        return self.pg

    def responde(self, corpo, status=200):
        self.resposta_pagamento = {"status": status, "corpo": corpo}

    def envia(self, dados):
        self.pg.evaluate("(d) => window.__enviar(d)", dados)
        self.pg.wait_for_timeout(500)

    def texto_erro(self):
        return self.pg.inner_text("#erro-pagamento") if self.pg.query_selector("#erro-pagamento") else ""

    def fecha(self):
        self.pg.close()


CARTAO = {"selectedPaymentMethod": "credit_card",
          "formData": {"token": "tok_de_teste", "payment_method_id": "master", "installments": 3,
                       "issuer_id": "24", "payer": {"email": "marcelo@example.com",
                                                    "identification": {"type": "CPF", "number": "12345678909"}}}}
PIX = {"selectedPaymentMethod": "bank_transfer",
       "formData": {"payment_method_id": "pix", "payer": {"email": "marcelo@example.com"}}}


def mede_estrutura(pg, erros_js, celular, rotulo):
    m = pg.evaluate("""() => {
      const q = (s) => Array.from(document.querySelectorAll(s));
      const mortos = q('a[href^="#"]').filter(a => a.getAttribute('href').length > 1 && !document.querySelector(a.getAttribute('href'))).map(a => a.getAttribute('href'));
      const imgs = q('img').filter(i => i.offsetParent !== null || i.getAttribute('src')).map(i => ({alt: i.hasAttribute('alt'), w: i.getAttribute('width'), h: i.getAttribute('height')}));
      const toque = q('button, input:not([type=hidden]), select, textarea, a.cta, a[role=button]')
        .filter(e => !e.closest('#brick'))
        .map(e => { const r = e.getBoundingClientRect(); return {tag: e.tagName, h: Math.round(r.height), txt: (e.innerText||e.placeholder||'').slice(0,24)}; })
        .filter(x => x.h > 0);
      return { scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth,
               h1: q('h1').length, imgs, mortos, toque, titulo: document.title,
               noindex: !!document.querySelector('meta[name=robots][content*=noindex]'),
               lang: document.documentElement.lang };
    }""")
    t(f"{rotulo} sem estouro horizontal", m["scrollW"] <= m["innerW"], f"{m['scrollW']} ≤ {m['innerW']}")
    t(f"{rotulo} um h1 só", m["h1"] == 1, m["h1"])
    t(f"{rotulo} lang pt-BR", m["lang"] == "pt-BR", m["lang"])
    t(f"{rotulo} noindex", m["noindex"])
    t(f"{rotulo} imagens com alt, width e height", all(i["alt"] and i["w"] and i["h"] for i in m["imgs"]), f"{len(m['imgs'])} img")
    t(f"{rotulo} sem âncora morta", not m["mortos"], m["mortos"] or "-")
    t(f"{rotulo} sem erro de JavaScript", not erros_js, erros_js[:2] or "-")
    if celular:
        baixos = [x for x in m["toque"] if x["h"] < 44]
        t(f"{rotulo} alvos de toque ≥ 44 px", not baixos,
          [f"{x['tag']} {x['h']}px {x['txt']!r}" for x in baixos][:5] or f"{len(m['toque'])} alvos")


def sem_travessao():
    print("\n═══ Texto: travessão no meio de frase")
    for nome in ("checkout.html", "obrigado.html", "assets/checkout.js", "assets/checkout.css"):
        bruto = open(os.path.join(RAIZ, nome), encoding="utf-8").read()
        achados = [c for c in ("—", "–", "&mdash;", "&ndash;") if c in bruto]
        t(f"{nome} sem travessão", not achados, achados or "-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--real-sdk", action="store_true", help="usa o SDK e a chave pública de verdade")
    a = ap.parse_args()
    os.makedirs(os.path.join(AQUI, "capturas"), exist_ok=True)
    srv, base = sobe_servidor()

    with sync_playwright() as p:
        nav = p.chromium.launch()

        # ── 1. Estrutura e sessão válida, nos três tamanhos ──────────────────
        for nome, (w, h) in TAMANHOS.items():
            ctx = nav.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                  permissions=["clipboard-read", "clipboard-write"],
                                  user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36" if w < 800 else None)
            c = Cenario(ctx, base)
            pg = c.abre()
            pg.wait_for_timeout(400)
            print(f"\n═══ checkout {nome}")
            mede_estrutura(pg, c.erros_js, w < 800, "")
            t("Brick montado", pg.eval_on_selector("#brick", "e => e.children.length > 0"))
            t("estado 'carregando' sumiu", pg.eval_on_selector("#estado", "e => e.hidden === true"))
            t("valor da tela veio do servidor", "97,00" in pg.inner_text("#valor"), pg.inner_text("#valor"))
            t("primeiro nome na saudação", "Marcelo" in pg.inner_text("#saudacao"))
            t("faixa de teste apagada", pg.eval_on_selector("#faixa-teste", "e => e.hidden === true"))
            t("recusa escondida", pg.eval_on_selector("#recusa", "e => e.hidden === true"))
            t("Pix escondido", pg.eval_on_selector("#pix", "e => e.hidden === true"))
            t("CPF escondido", pg.eval_on_selector("#cpf-bloco", "e => e.hidden === true"))
            cfg = pg.evaluate("() => window.__config ? {amount: window.__config.initialization.amount, "
                              "metodos: Object.keys(window.__config.customization.paymentMethods), "
                              "parcelas: window.__config.customization.paymentMethods.maxInstallments, "
                              "tema: window.__config.customization.visual.style.theme, "
                              "vars: window.__config.customization.visual.style.customVariables} : null")
            t("amount do Brick = valor da sessão", cfg and cfg["amount"] == 97, cfg and cfg["amount"])
            t("maxInstallments = max_parcelas da sessão", cfg and cfg["parcelas"] == 6, cfg and cfg["parcelas"])
            t("tema dark", cfg and cfg["tema"] == "dark")
            t("meios excluídos saíram do objeto (sem lista vazia)",
              cfg and sorted(cfg["metodos"]) == ["bankTransfer", "creditCard", "maxInstallments"], cfg and cfg["metodos"])
            # 08/09: a asserção comparava com valores FIXOS do Nocturne e quebrou quando o Jean
            # pediu a paleta da Clinix. O código sempre esteve certo: ele lê o token vivo. Então
            # o teste passa a ler o token vivo também, e assim ele continua valendo em qualquer
            # paleta futura. 🔑 Teste que fixa o valor do tema vira teste que proíbe trocar de tema.
            tokens = pg.evaluate("() => { const c = getComputedStyle(document.documentElement);\n                const v = (n) => c.getPropertyValue(n).trim();\n                return {superficie: v('--color-surface'), fundo: v('--color-bg'), acento: v('--color-accent')}; }")
            t("customVariables leem os tokens VIVOS da página",
              cfg and cfg["vars"]["formBackgroundColor"] == tokens["superficie"]
                  and cfg["vars"]["inputBackgroundColor"] == tokens["fundo"]
                  and cfg["vars"]["baseColor"] == tokens["acento"],
              f'fundo do formulário {cfg and cfg["vars"]["formBackgroundColor"]} = token {tokens["superficie"]}')
            t("sem vazamento para produção", not c.vazamentos, c.vazamentos[:2] or "-")
            pg.screenshot(path=os.path.join(AQUI, "capturas", f"checkout-{nome}.png"), full_page=True)
            c.fecha(); ctx.close()

        ctx = nav.new_context(viewport={"width": 390, "height": 844},
                              permissions=["clipboard-read", "clipboard-write"])

        # ── 2. Sessão de teste ───────────────────────────────────────────────
        print("\n═══ sessão de teste (valor 1)")
        teste = dict(SESSAO_OK, valor=1, teste=True)
        c = Cenario(ctx, base, sessao=teste); pg = c.abre(); pg.wait_for_timeout(400)
        t("faixa de teste acesa", pg.eval_on_selector("#faixa-teste", "e => e.hidden === false"))
        t("valor de teste na tela", "1,00" in pg.inner_text("#valor"), pg.inner_text("#valor"))
        c.fecha()

        # ── 3. Sessão vencida ────────────────────────────────────────────────
        print("\n═══ sessão vencida (404)")
        c = Cenario(ctx, base, sessao={"ok": False, "codigo": "SESSAO_EXPIRADA_OU_INEXISTENTE"}, codigo_sessao=404)
        pg = c.abre(); pg.wait_for_timeout(500)
        t("recusa aparece", pg.eval_on_selector("#recusa", "e => e.hidden === false"))
        t("recusa explica o vencimento", "não vale mais" in pg.inner_text("#recusa-texto"), pg.inner_text("#recusa-texto")[:60])
        t("Brick NÃO foi montado", pg.eval_on_selector("#brick", "e => e.children.length === 0"))
        t("caminho de volta para a página de venda", "index.html" in (pg.get_attribute("#recusa-volta", "href") or ""))
        t("a linha do total sai da tela (nada de 'carregando' eterno)", pg.eval_on_selector("#total", "e => e.hidden === true"))
        t("sem erro de JavaScript", not c.erros_js, c.erros_js[:2] or "-")
        pg.screenshot(path=os.path.join(AQUI, "capturas", "checkout-sessao-vencida.png"), full_page=True)
        c.fecha()

        # ── 4. Mercado Pago desligado ────────────────────────────────────────
        print("\n═══ Mercado Pago desligado (503)")
        c = Cenario(ctx, base, sessao={"ok": False, "codigo": "MP_DESLIGADO"}, codigo_sessao=503)
        pg = c.abre(); pg.wait_for_timeout(500)
        t("recusa aparece", pg.eval_on_selector("#recusa", "e => e.hidden === false"))
        t("texto fala de fora do ar", "fora do ar" in pg.inner_text("#recusa-texto"), pg.inner_text("#recusa-texto")[:60])
        t("Brick NÃO foi montado", pg.eval_on_selector("#brick", "e => e.children.length === 0"))
        c.fecha()

        # ── 5. Sem token na URL ──────────────────────────────────────────────
        print("\n═══ endereço sem token")
        c = Cenario(ctx, base); pg = c.abre(query=""); pg.wait_for_timeout(400)
        t("recusa aparece", pg.eval_on_selector("#recusa", "e => e.hidden === false"))
        t("Brick NÃO foi montado", pg.eval_on_selector("#brick", "e => e.children.length === 0"))
        t("não perguntou nada ao servidor", not c.envios)
        c.fecha()

        # ── 6. Cartão aprovado ───────────────────────────────────────────────
        print("\n═══ cartão aprovado")
        c = Cenario(ctx, base); pg = c.abre(); pg.wait_for_timeout(400)
        c.responde({"ok": True, "payment_id": "123456789", "status": "approved",
                    "status_detail": "accredited", "metodo": "credit_card"})
        c.envia(CARTAO)
        pg.wait_for_timeout(600)
        t("foi para obrigado.html", "obrigado.html" in pg.url, pg.url.split("/")[-1][:60])
        t("levou o payment_id na URL", "p=123456789" in pg.url)
        corpo = json.loads(c.envios[-1]) if c.envios else {}
        t("corpo: idempotência é UUID v4", UUID4.match(str(corpo.get("idempotencia", ""))), corpo.get("idempotencia"))
        t("corpo: token da sessão", corpo.get("token_sessao") == TOKEN)
        t("corpo: tipo credit_card", corpo.get("tipo") == "credit_card", corpo.get("tipo"))
        t("corpo: token do cartão", corpo.get("token") == "tok_de_teste")
        t("corpo: payment_method_id", corpo.get("payment_method_id") == "master")
        t("corpo: parcelas", corpo.get("installments") == 3, corpo.get("installments"))
        t("corpo: issuer_id", corpo.get("issuer_id") == "24")
        t("corpo: e-mail", corpo.get("email") == "marcelo@example.com")
        t("corpo: CPF do formulário do Brick", corpo.get("cpf") == "12345678909", corpo.get("cpf"))
        t("corpo: device id", corpo.get("device_id") == "device-de-teste", corpo.get("device_id"))
        t("corpo: nenhum dado de cartão", not re.search(r"card_number|security_code|cvv", c.envios[-1], re.I))
        # ⚠️ O preflight NÃO se prova aqui: quando o Playwright responde por uma
        #    rota, o Chromium não dispara o OPTIONS (o contador `preflights` fica
        #    zerado de propósito). Quem provou foi o mundo real, com
        #    `curl -X OPTIONS https://n8n-webhook.clinixsystem.com.br/webhook/wcp/pagamento/criar`
        #    em 08/09/2026: 204, `access-control-allow-headers: content-type`,
        #    `access-control-allow-methods: OPTIONS, POST`. Por isso o corpo vai em
        #    JSON, e não em formulário.
        t("o teste não fingiu preflight que não houve", len(c.preflights) == 0, len(c.preflights))
        c.fecha()

        # ── 7. Idempotência nova a cada envio ────────────────────────────────
        print("\n═══ idempotência por tentativa")
        c = Cenario(ctx, base); pg = c.abre(); pg.wait_for_timeout(400)
        c.responde({"ok": True, "payment_id": "1", "status": "rejected", "status_detail": "cc_rejected_other_reason"})
        c.envia(CARTAO); c.envia(CARTAO)
        ids = [json.loads(x).get("idempotencia") for x in c.envios]
        t("dois envios, duas idempotências diferentes", len(ids) == 2 and ids[0] != ids[1], ids)
        c.fecha()

        # ── 8. Recusado: motivo em português e o formulário continua ─────────
        print("\n═══ cartão recusado")
        for detalhe, pedaco in (("cc_rejected_bad_filled_security_code", "código de segurança"),
                                ("cc_rejected_insufficient_amount", "limite"),
                                ("cc_rejected_call_for_authorize", "autorizar"),
                                ("cc_rejected_bad_filled_date", "validade"),
                                ("cc_rejected_bad_filled_card_number", "número do cartão"),
                                ("cc_rejected_high_risk", "não autorizou"),
                                ("cc_rejected_other_reason", "não disse o motivo")):
            c = Cenario(ctx, base); pg = c.abre(); pg.wait_for_timeout(400)
            c.responde({"ok": True, "payment_id": "1", "status": "rejected", "status_detail": detalhe})
            c.envia(CARTAO)
            texto = c.texto_erro()
            t(f"{detalhe} → motivo em português", pedaco in texto, texto[:70])
            t(f"{detalhe} → o formulário continua na tela",
              pg.eval_on_selector("#brick", "e => e.children.length > 0"))
            t(f"{detalhe} → o Brick recebe 'tenta de novo'",
              pg.evaluate("() => window.__submit") == "tenta de novo", pg.evaluate("() => window.__submit"))
            c.fecha()

        # ── 9. Pix ───────────────────────────────────────────────────────────
        print("\n═══ Pix")
        c = Cenario(ctx, base); pg = c.abre(); pg.wait_for_timeout(400)
        # 9.1 o Brick do Pix não traz CPF: a nossa página pede
        c.envia(PIX)
        t("sem CPF o Pix não é enviado ao servidor", not c.envios, len(c.envios))
        t("a página pede o CPF", pg.eval_on_selector("#cpf-bloco", "e => e.hidden === false"))
        t("o recado do CPF não é vermelho", "aviso" in (pg.get_attribute("#erro-pagamento", "class") or ""))
        # 9.2 com o CPF preenchido, o nosso botão gera o Pix
        qr = ("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
        c.responde({"ok": True, "payment_id": "987", "status": "pending", "status_detail": "pending_waiting_transfer",
                    "metodo": "bank_transfer",
                    "pix": {"qr_code": "00020126580014BR.GOV.BCB.PIX0136teste-copia-e-cola-do-workshop5204000053039865802BR",
                            "qr_code_base64": qr, "ticket_url": "https://www.mercadopago.com.br/payments/987/ticket",
                            "expira_em": "2026-09-08T18:30:00.000-03:00"}})
        pg.fill("#cpf", "12345678909")
        pg.click("#cpf-segue")
        pg.wait_for_timeout(700)
        corpo = json.loads(c.envios[-1]) if c.envios else {}
        t("corpo do Pix: tipo bank_transfer", corpo.get("tipo") == "bank_transfer", corpo.get("tipo"))
        t("corpo do Pix: payment_method_id pix", corpo.get("payment_method_id") == "pix")
        t("corpo do Pix: CPF que a pessoa digitou", corpo.get("cpf") == "12345678909", corpo.get("cpf"))
        t("corpo do Pix: sem token de cartão", corpo.get("token") == "")
        t("QR na tela", pg.eval_on_selector("#pix", "e => e.hidden === false"))
        t("QR é imagem embutida", (pg.get_attribute("#pix-qr", "src") or "").startswith("data:image/png;base64,"))
        t("copia e cola preenchido", "BR.GOV.BCB.PIX" in (pg.input_value("#pix-codigo") or ""))
        t("prazo na tela", "vale até" in pg.inner_text("#pix-prazo"), pg.inner_text("#pix-prazo"))
        t("o Brick foi desmontado", pg.evaluate("() => window.__desmontado === true"))
        pg.click("#pix-copiar"); pg.wait_for_timeout(400)
        t("botão de copiar avisa que copiou", "copiado" in pg.inner_text("#pix-copiado").lower(), pg.inner_text("#pix-copiado")[:50])
        copiado = pg.evaluate("() => navigator.clipboard.readText()")
        t("a área de transferência tem o código do Pix", "BR.GOV.BCB.PIX" in copiado, copiado[:40])
        t("aviso de que pode fechar a página sem perder a compra",
          "não perde a compra" in pg.inner_text("#pix"))
        pg.screenshot(path=os.path.join(AQUI, "capturas", "checkout-pix.png"), full_page=True)
        c.fecha()

        # ── 10. Erros do servidor ────────────────────────────────────────────
        print("\n═══ erros do servidor")
        for status, corpo_erro, pedaco in ((429, {"ok": False, "codigo": "MUITAS_TENTATIVAS"}, "muitas tentativas"),
                                           (502, {"ok": False, "codigo": "PAGAMENTO_INDISPONIVEL"}, "não foi criada"),
                                           (503, {"ok": False, "codigo": "MP_DESLIGADO"}, "fora do ar"),
                                           (400, {"ok": False, "codigo": "CPF_INVALIDO"}, "11 dígitos"),
                                           (400, {"ok": False, "codigo": "EMAIL_INVALIDO"}, "e-mail")):
            c = Cenario(ctx, base); pg = c.abre(); pg.wait_for_timeout(400)
            c.responde(corpo_erro, status=status)
            c.envia(CARTAO)
            texto = c.texto_erro().lower()
            t(f"{status} {corpo_erro['codigo']} → recado certo", pedaco.lower() in texto, texto[:70])
            t(f"{status} {corpo_erro['codigo']} → o formulário continua na tela",
              pg.eval_on_selector("#brick", "e => e.children.length > 0"))
            c.fecha()

        # sessão que vence no meio do pagamento: a tela troca para a recusa
        c = Cenario(ctx, base); pg = c.abre(); pg.wait_for_timeout(400)
        c.responde({"ok": False, "codigo": "SESSAO_EXPIRADA_OU_INEXISTENTE"}, status=400)
        c.envia(CARTAO); pg.wait_for_timeout(400)
        t("400 SESSAO_EXPIRADA no envio → recusa e Brick desmontado",
          pg.eval_on_selector("#recusa", "e => e.hidden === false") and pg.evaluate("() => window.__desmontado === true"))
        c.fecha()

        # ── 11. Pagamento em análise ─────────────────────────────────────────
        print("\n═══ pagamento em análise")
        c = Cenario(ctx, base); pg = c.abre(); pg.wait_for_timeout(400)
        c.responde({"ok": True, "payment_id": "77", "status": "in_process", "status_detail": "pending_review_manual"})
        c.envia(CARTAO)
        t("diz que está em análise", "análise" in c.texto_erro(), c.texto_erro()[:70])
        t("avisa que não precisa pagar de novo", "não precisa pagar de novo" in c.texto_erro())
        t("recado neutro, não vermelho", "aviso" in (pg.get_attribute("#erro-pagamento", "class") or ""))
        c.fecha()

        # ── 12. obrigado.html ────────────────────────────────────────────────
        print("\n═══ obrigado.html")
        c = Cenario(ctx, base); pg = c.abre("obrigado.html", "?p=123456789"); pg.wait_for_timeout(300)
        mede_estrutura(pg, c.erros_js, True, "")
        t("não mostra o p= da URL em lugar nenhum", "123456789" not in pg.inner_text("body"))
        t("diz quem libera o acesso", "não esta página" in pg.inner_text("body"))
        t("tem a data do workshop", "19 de outubro" in pg.inner_text("body"))
        marcas = pg.eval_on_selector_all(".pendente", "e => e.length")
        faixa = pg.inner_text(".faixa")
        # a faixa é caixa alta por CSS: compara sem diferenciar maiúscula
        t("a contagem da faixa bate com as marcas do DOM", f"{marcas} pendências" in faixa.lower(), f"{marcas} × {faixa}")
        pg.screenshot(path=os.path.join(AQUI, "capturas", "obrigado-390x844.png"), full_page=True)
        c.fecha()
        ctx.close()

        # ── 13. O Brick de verdade (só com --real-sdk) ───────────────────────
        if a.real_sdk:
            print("\n═══ Brick de verdade (SDK e chave pública reais)")
            chave = ""
            caminho = os.path.expanduser("~/.config/n8n-producao/mercadopago-publica.env")
            for linha in open(caminho, encoding="utf-8"):
                if linha.startswith("MP_PUBLIC_KEY="):
                    chave = linha.split("=", 1)[1].strip()
            t("chave pública encontrada no disco", bool(chave), f"{len(chave)} caracteres")
            ctx = nav.new_context(viewport={"width": 390, "height": 844})
            c = Cenario(ctx, base, sessao=dict(SESSAO_OK, public_key=chave), real_sdk=True)
            # no modo real o SDK e a API do Mercado Pago podem sair; o nosso servidor, não
            c.pg.unroute("https://api.mercadopago.com/**")
            respostas = []
            c.pg.on("response", lambda r: respostas.append((r.status, r.url[:90])) if "mercadopago" in r.url else None)
            pg = c.abre()
            # 🔑 Não basta o "carregando" sumir: o vigia de 20 s também o esconde
            #    quando desiste. A prova é o formulário estar DENTRO do #brick e a
            #    recusa continuar escondida. (Este item já foi um falso positivo.)
            try:
                pg.wait_for_function(
                    "() => document.getElementById('brick').children.length > 0"
                    " && document.getElementById('recusa').hidden === true", timeout=30000)
                pronto = True
            except Exception:
                pronto = False
            ruins = [r for r in respostas if r[0] >= 400]
            t("o Brick de verdade abriu (formulário dentro de #brick)", pronto,
              (ruins[:1] or [pg.inner_text('#recusa-texto')[:60]]))
            pg.screenshot(path=os.path.join(AQUI, "capturas", "checkout-brick-real.png"), full_page=True)
            c.fecha(); ctx.close()

        nav.close()
    srv.shutdown()

    sem_travessao()
    print(f"\n{ok_n} ✅ · {ruim_n} 🔴")
    return 1 if ruim_n else 0


if __name__ == "__main__":
    sys.exit(main())
