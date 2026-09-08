#!/usr/bin/env python3
"""Prova a página de venda num navegador de verdade (Chromium do Playwright).

    python3 testes/medir.py                       # arquivo local index.html, 3 tamanhos, sem enviar nada
    python3 testes/medir.py --url https://…       # a página publicada
    python3 testes/medir.py --enviar              # preenche o formulário com telefone de TESTE e envia de verdade
    python3 testes/medir.py --simular             # intercepta o POST e responde {ok,next} falso: prova o redirecionamento

O que mede (e imprime ✅/🔴 por item):
- estouro horizontal em 360×640, 390×844 e 1440×900 (scrollWidth ≤ innerWidth)
- um h1 só; todo <img> com alt, width e height; nenhum link interno morto (#âncora sem alvo)
- alvo de toque: botões, links de navegação e inputs com altura ≥ 44 px no celular
- formulário: campos, honeypot escondido de gente, aceite obrigatório no NAVEGADOR (o servidor já recusa)
- o POST leva consentimento=1, politica_versao, utm_*, fbclid, pagina (lidos da URL)
- com --simular: a resposta {ok:true,next} redireciona para next
- toda <img> carregou de verdade (naturalWidth > 0), nao so existe no HTML
- as ilustracoes SVG desenhadas por nos tem area na tela, e nenhum grupo delas
  esta colapsado — `scale(0)` esconde exatamente como `opacity: 0` esconde
- a grade de orcamentos tem 490 pontos EXATOS (35 x 14 no <pattern>)
- as 9 secoes existem por id, os 5 cartoes existem, e a faixa amarela conta as
  pendencias que estao mesmo no DOM
- TODO numero da tela e igual ao `data-conta` dele: a contagem animada nunca
  pode deixar um valor intermediario pintado numa pagina que vende numero real
- contraste AA (>= 4,5:1) calculado sobre a cor efetivamente pintada, em 9 papeis
  de texto de corpo
- travessao no meio de frase: zero, no HTML, no CSS e no JavaScript da pagina
- capturas em testes/capturas/<tamanho>.png. NAO sao `full_page`: o modo de
  pagina inteira do Chromium deixa de pintar imagem que nunca esteve no viewport.
  O teste rola a pagina, estica o viewport ate a altura do documento e so entao
  fotografa, com as animacoes congeladas no estado final.

⛔ --enviar usa SEMPRE telefone da faixa de teste (+55 38 99000-00xx). Nunca telefone real.
"""
import argparse, json, os, sys, time
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
TAMANHOS = {"360x640": (360, 640), "390x844": (390, 844), "1440x900": (1440, 900)}
TEL_TESTE = "(38) 99000-0007"
ok_n = ruim_n = 0


def t(rotulo, cond, extra=""):
    global ok_n, ruim_n
    ok_n += cond; ruim_n += (not cond)
    print(f"{'✅' if cond else '🔴'} {rotulo}{(' · ' + str(extra)) if extra else ''}")


def sem_travessao():
    """Travessao no meio de frase e proibido na frente Workshop (cofre,
    20 Estrategia/Restricoes de Conteudo). A regra vale para o ARQUIVO INTEIRO,
    comentario incluso, e nao so para o texto visivel: o mesmo teste ja roda
    assim no checkout, e um travessao esquecido num comentario e o que mais
    facilmente vira travessao numa frase quando alguem copia o trecho."""
    print("\n═══ Texto: travessão no meio de frase")
    for nome in ("index.html", "assets/estilo.css", "assets/pagina.js",
                 "assets/newsreader.css", "assets/inter.css", "privacidade.html"):
        bruto = open(os.path.join(RAIZ, nome), encoding="utf-8").read()
        achados = [c for c in ("—", "–", "&mdash;", "&ndash;") if c in bruto]
        t(f"{nome} sem travessão", not achados, achados or "-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url"); ap.add_argument("--enviar", action="store_true"); ap.add_argument("--simular", action="store_true")
    a = ap.parse_args()
    alvo = a.url or ("file://" + os.path.join(RAIZ, "index.html"))
    if not a.url: alvo += "?utm_source=prova&utm_medium=teste&utm_campaign=medir&fbclid=fb.teste"
    os.makedirs(os.path.join(AQUI, "capturas"), exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for nome, (w, h) in TAMANHOS.items():
            ctx = nav.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                  user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36" if w < 800 else None)
            pg = ctx.new_page(); erros_js = []
            pg.on("pageerror", lambda e: erros_js.append(str(e)))
            pg.goto(alvo, wait_until="load"); pg.wait_for_timeout(600)
            # Rola a página inteira ANTES de medir e de fotografar. Duas razões,
            # as duas aprendidas na marra em 08/09:
            #  1. imagem `loading=lazy` fora do viewport não carrega, e a captura
            #     de página inteira sai com buraco no lugar dela;
            #  2. animação de entrada por IntersectionObserver não dispara para o
            #     que nunca esteve na tela — foi assim que duas ilustrações
            #     apareceram como retângulo vazio e ninguém viu.
            pg.evaluate("""async () => {
              // A captura de pagina inteira do Chromium NAO pinta imagem
              // `loading=lazy`, mesmo ja carregada: sai buraco no lugar dela e
              // quem olha a captura jura que a pagina esta quebrada. Medido em
              // 08/09 com a planilha da secao "A conta". Por isso o teste tira o
              // lazy de todas ANTES de rolar. A pagina em producao segue lazy.
              document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; });
              const passo = Math.round(window.innerHeight * 0.8);
              for (let y = 0; y < document.body.scrollHeight; y += passo) {
                window.scrollTo(0, y);
                await new Promise(r => setTimeout(r, 90));
              }
              window.scrollTo(0, 0);
              await new Promise(r => setTimeout(r, 300));
              // espera cada imagem terminar de carregar, com teto de 4 s por imagem.
              // Sem isto o teste fotografa buraco e diz que esta tudo bem.
              // ATENCAO: `decode()` sozinho NAO serve: numa imagem `lazy` que ainda
              // nem comecou a baixar ele fica pendente para sempre e trava o teste.
              const teto = (pr) => Promise.race([pr, new Promise(r => setTimeout(r, 4000))]);
              await Promise.all(Array.from(document.images).map(i => {
                if (i.complete && i.naturalWidth) return null;
                i.loading = 'eager';
                return teto(new Promise(r => { i.addEventListener('load', r, {once: true});
                                               i.addEventListener('error', r, {once: true}); }));
              }));
            }""")
            pg.wait_for_timeout(700)
            m = pg.evaluate("""() => {
              const q = (s) => Array.from(document.querySelectorAll(s));
              const mortos = q('a[href^="#"]').filter(a => a.getAttribute('href').length > 1 && !document.querySelector(a.getAttribute('href'))).map(a => a.getAttribute('href'));
              const imgs = q('img').map(i => ({alt: i.hasAttribute('alt'), w: i.getAttribute('width'), h: i.getAttribute('height'),
                                               src: i.getAttribute('src'), carregou: i.complete && i.naturalWidth > 0}));
              // Ilustrações SVG desenhadas por nós: têm de estar com área na tela.
              // `scale(0)` esconde igualzinho a `opacity: 0` — esta asserção existe
              // porque a primeira versão fez exatamente isso e passou despercebido.
              const ilustras = q('.ilustra, .cartao-fig').map(s => { const r = s.getBoundingClientRect();
                return {cls: s.getAttribute('class'), w: Math.round(r.width), h: Math.round(r.height)}; });
              const escondidas = q('.ilustra g, .cartao-fig g').map(g => { const r = g.getBoundingClientRect();
                return {w: Math.round(r.width), h: Math.round(r.height)}; }).filter(x => x.w === 0 || x.h === 0);
              // A grade de orçamentos é 35 × 14 = 490 pontos EXATOS. Se alguém mexer
              // no <pattern> ou no <rect>, o número da tela deixa de ser o número real.
              const pat = document.querySelector('#orcamentos');
              const rectOrc = document.querySelector('.pontos-cortina rect');
              const pontos = (pat && rectOrc)
                ? (parseFloat(rectOrc.getAttribute('width')) / parseFloat(pat.getAttribute('width'))) *
                  (parseFloat(rectOrc.getAttribute('height')) / parseFloat(pat.getAttribute('height'))) : null;
              // Seções da página, por id, na ordem em que têm de aparecer.
              const secoes = ['topo','para-quem','a-conta','o-que-acontece','nao-vou-fazer','quem-faz','detalhes','faq','inscricao']
                .filter(id => !document.getElementById(id));
              // O NUMERO DA TELA E O NUMERO DECLARADO. A animacao de contagem
              // sobe de zero ate o valor; se ela parar no meio (aba em segundo
              // plano, rAF suspenso), a pessoa le um numero que nao existe. Numa
              // pagina que vende "os numeros sao os reais da minha clinica" isso
              // e defeito de conteudo, nao de layout. Aqui se confere o texto
              // pintado contra o proprio `data-conta`.
              const fmtBR = { int:  v => Math.round(v).toLocaleString('pt-BR'),
                              brl0: v => 'R$ ' + Math.round(v).toLocaleString('pt-BR'),
                              brl2: v => 'R$ ' + v.toLocaleString('pt-BR', {minimumFractionDigits:2, maximumFractionDigits:2}) };
              const numerosErrados = q('[data-conta]').map(el => {
                const esperado = (fmtBR[el.dataset.formato] || fmtBR.int)(parseFloat(el.dataset.conta));
                return el.textContent.trim() === esperado ? null : {viu: el.textContent.trim(), esperava: esperado};
              }).filter(Boolean);
              const cartoes = q('.cartoes .cartao').length;
              const pendencias = q('.pendente').length;
              const contadorFaixa = parseInt((document.getElementById('n-pendencias')||{}).textContent, 10);
              // Contraste calculado, não estimado (WCAG 2.x sobre a cor efetivamente pintada).
              const lum = (c) => { const [r,g,b] = c.match(/\\d+(\\.\\d+)?/g).slice(0,3).map(Number)
                  .map(v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
                return 0.2126*r + 0.7152*g + 0.0722*b; };
              const fundoDe = (el) => { let n = el;
                while (n && n !== document.documentElement) {
                  const bg = getComputedStyle(n).backgroundColor;
                  if (bg && !/rgba\\(0, 0, 0, 0\\)|transparent/.test(bg)) return bg;
                  n = n.parentElement; }
                return getComputedStyle(document.body).backgroundColor || 'rgb(22, 24, 38)'; };
              const razao = (el) => { const a = lum(getComputedStyle(el).color), b = lum(fundoDe(el));
                return Math.round(((Math.max(a,b)+0.05)/(Math.min(a,b)+0.05)) * 100) / 100; };
              const contrastes = [['.lead','.lead'],['.corpo','.corpo'],['.miudo','.miudo'],
                                  ['.cartao-b','.cartao-b'],['.quadro-legenda','.quadro-legenda'],
                                  ['.numeros dd','.numeros dd'],['.resposta p','.resposta p'],
                                  ['.rodape p','.rodape p'],['.detalhes dd','.detalhes dd']]
                .map(([rot, sel]) => { const el = document.querySelector(sel);
                  return el ? {rot, r: razao(el)} : null; }).filter(Boolean);
              const toque = q('button, input:not([type=hidden]), select, textarea, a.cta, a[role=button]').map(e => { const r = e.getBoundingClientRect(); return {tag: e.tagName, h: Math.round(r.height), txt: (e.innerText||e.placeholder||'').slice(0,20)}; }).filter(x => x.h > 0);
              const hp = document.querySelector('[name=site_url]');
              const hpVisivel = hp ? (hp.getBoundingClientRect().width > 0 && getComputedStyle(hp).visibility !== 'hidden' && getComputedStyle(hp).display !== 'none' && hp.getBoundingClientRect().left >= 0) : null;
              return { scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth, h1: q('h1').length,
                       imgs, mortos, toque, hp: !!hp, hpVisivel, form: !!document.querySelector('form'),
                       campos: q('form input[name], form select[name]').map(i => i.name), titulo: document.title,
                       noindex: !!document.querySelector('meta[name=robots][content*=noindex]'), lang: document.documentElement.lang,
                       ilustras, escondidas, pontos, secoes, cartoes, pendencias, contadorFaixa, contrastes,
                       numerosErrados, nConta: q('[data-conta]').length };
            }""")
            print(f"\n═══ {nome} · {m['titulo'][:60]}")
            t("sem estouro horizontal", m["scrollW"] <= m["innerW"], f"{m['scrollW']} ≤ {m['innerW']}")
            t("um h1 só", m["h1"] == 1, m["h1"])
            t("lang pt-BR", m["lang"] == "pt-BR", m["lang"])
            t("noindex (versão de trabalho)", m["noindex"])
            t("imagens com alt, width e height", all(i["alt"] and i["w"] and i["h"] for i in m["imgs"]), f"{len(m['imgs'])} img")
            nao_carregou = [i["src"] for i in m["imgs"] if not i["carregou"]]
            t("toda imagem carregou de verdade", not nao_carregou, nao_carregou or f"{len(m['imgs'])} img")
            t("sem âncora morta", not m["mortos"], m["mortos"] or "-")
            t("sem erro de JavaScript", not erros_js, erros_js[:2] or "-")
            # ── as ilustrações e as seções (acrescentado em 08/09) ──────────────
            sem_area = [i for i in m["ilustras"] if i["w"] < 40 or i["h"] < 20]
            t("ilustrações SVG com área na tela", not sem_area, sem_area[:3] or f"{len(m['ilustras'])} peças")
            t("nenhum grupo de ilustração colapsado (scale(0) esconde igual a opacity 0)",
              not m["escondidas"], m["escondidas"][:3] or "-")
            t("a grade de orçamentos tem 490 pontos exatos", m["pontos"] == 490, m["pontos"])
            t("todas as seções presentes", not m["secoes"], m["secoes"] or "9 seções")
            t("os cinco cartões dos cinco números", m["cartoes"] == 5, m["cartoes"])
            t("todo número da tela é o número declarado em data-conta",
              not m["numerosErrados"], m["numerosErrados"][:3] or f"{m['nConta']} números")
            t("a faixa conta as pendências que existem no DOM",
              m["contadorFaixa"] == m["pendencias"], f"faixa {m['contadorFaixa']} · DOM {m['pendencias']}")
            ruins = [c for c in m["contrastes"] if c["r"] < 4.5]
            t("contraste AA (≥ 4,5:1) em todo texto de corpo", not ruins,
              [f"{c['rot']} {c['r']}:1" for c in ruins] or
              " · ".join(f"{c['rot']} {c['r']}:1" for c in m["contrastes"]))
            if w < 800:
                baixos = [x for x in m["toque"] if x["h"] < 44]
                t("alvos de toque ≥ 44 px", not baixos, [f"{x['tag']} {x['h']}px {x['txt']!r}" for x in baixos][:5] or f"{len(m['toque'])} alvos")
            t("formulário presente", m["form"])
            t("honeypot site_url existe e está escondido de gente", m["hp"] and m["hpVisivel"] is False)
            for c in ("nome", "telefone", "email", "consentimento", "politica_versao", "utm_source", "utm_medium", "utm_campaign", "fbclid", "pagina", "site_url"):
                t(f"  campo {c}", c in m["campos"])
            # 🔑 A captura NÃO é `full_page=True`. Medido em 08/09: o modo de
            # página inteira do Chromium deixa de pintar imagem que nunca esteve
            # no viewport — as três ilustrações 3D da seção "A conta" saíam como
            # retângulo vazio, e quem olhasse a captura concluiria que a página
            # estava quebrada. O caminho honesto é esticar o viewport até a
            # altura do documento e fotografar o que o navegador realmente pinta.
            altura = min(pg.evaluate("() => document.documentElement.scrollHeight"), 20000)
            pg.set_viewport_size({"width": w, "height": altura})
            # `animations="disabled"` congela toda animação CSS no estado FINAL —
            # sem isso a captura pega a barra de horas crescendo pela metade e
            # parece defeito. A espera cobre a contagem dos números, que é rAF.
            pg.wait_for_timeout(2000)
            pg.screenshot(path=os.path.join(AQUI, "capturas", f"{nome}.png"), animations="disabled")
            pg.set_viewport_size({"width": w, "height": h})
            pg.wait_for_timeout(200)

            if nome == "390x844" and (a.enviar or a.simular):
                pedidos = []
                if a.simular:
                    def rota(route, request):
                        pedidos.append(request.post_data or "")
                        route.fulfill(status=200, content_type="application/json", body=json.dumps({"ok": True, "next": "https://example.com/pagamento-simulado"}))
                    pg.route("**/webhook/wcp/form/lead", rota)
                else:
                    pg.on("request", lambda r: pedidos.append(r.post_data or "") if "wcp/form/lead" in r.url else None)
                # 1. aceite desmarcado → o navegador segura
                pg.fill("input[name=nome]", "Teste Página"); pg.fill("input[name=telefone]", TEL_TESTE); pg.fill("input[name=email]", "teste-wcp@example.com")
                pg.click("form button[type=submit]"); pg.wait_for_timeout(500)
                t("sem aceite o navegador não envia", not pedidos, len(pedidos))
                # 2. com aceite → POST com tudo
                pg.check("input[name=consentimento]")
                if a.enviar: pg.fill("input[name=teste]", "1") if pg.query_selector("input[name=teste]") else None
                pg.click("form button[type=submit]")
                pg.wait_for_timeout(4000 if a.enviar else 1200)
                t("POST enviado", len(pedidos) >= 1)
                corpo = pedidos[-1] if pedidos else ""
                for k in ("consentimento=1", "politica_versao=", "utm_source=prova", "fbclid=fb.teste", "pagina=", "nome=", "telefone=", "email="):
                    t(f"  corpo tem {k}", k in corpo)
                t("  corpo NÃO tem site_url preenchido", "site_url=&" in corpo or corpo.endswith("site_url=") or "site_url" not in corpo)
                if a.simular:
                    pg.wait_for_timeout(800)
                    t("redirecionou para next", pg.url.startswith("https://example.com/pagamento-simulado"), pg.url)
                else:
                    # 08/09: o destino MUDOU. Antes o porteiro devolvia o link do Checkout Pro;
                    # agora ele devolve a NOSSA página de pagamento com o token da sessão, e o
                    # link do Mercado Pago virou reserva (o `montaResposta` do porteiro tenta os
                    # dois, nessa ordem). 🔑 Aceitar os dois é o certo: fixar um só transformaria
                    # este teste numa trava contra a própria rede de segurança.
                    destino_ok = "checkout.html?c=" in pg.url or "mercadopago.com" in pg.url
                    t("redirecionou para o pagamento (nossa página, ou o Mercado Pago como reserva)",
                      destino_ok, pg.url[:95])
            ctx.close()
        nav.close()
    sem_travessao()
    print(f"\n{ok_n} ✅ · {ruim_n} 🔴")
    return 1 if ruim_n else 0


if __name__ == "__main__":
    sys.exit(main())
