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
- capturas em testes/capturas/<tamanho>.png

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
            m = pg.evaluate("""() => {
              const q = (s) => Array.from(document.querySelectorAll(s));
              const mortos = q('a[href^="#"]').filter(a => a.getAttribute('href').length > 1 && !document.querySelector(a.getAttribute('href'))).map(a => a.getAttribute('href'));
              const imgs = q('img').map(i => ({alt: i.hasAttribute('alt'), w: i.getAttribute('width'), h: i.getAttribute('height')}));
              const toque = q('button, input:not([type=hidden]), select, textarea, a.cta, a[role=button]').map(e => { const r = e.getBoundingClientRect(); return {tag: e.tagName, h: Math.round(r.height), txt: (e.innerText||e.placeholder||'').slice(0,20)}; }).filter(x => x.h > 0);
              const hp = document.querySelector('[name=site_url]');
              const hpVisivel = hp ? (hp.getBoundingClientRect().width > 0 && getComputedStyle(hp).visibility !== 'hidden' && getComputedStyle(hp).display !== 'none' && hp.getBoundingClientRect().left >= 0) : null;
              return { scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth, h1: q('h1').length,
                       imgs, mortos, toque, hp: !!hp, hpVisivel, form: !!document.querySelector('form'),
                       campos: q('form input[name], form select[name]').map(i => i.name), titulo: document.title,
                       noindex: !!document.querySelector('meta[name=robots][content*=noindex]'), lang: document.documentElement.lang };
            }""")
            print(f"\n═══ {nome} · {m['titulo'][:60]}")
            t("sem estouro horizontal", m["scrollW"] <= m["innerW"], f"{m['scrollW']} ≤ {m['innerW']}")
            t("um h1 só", m["h1"] == 1, m["h1"])
            t("lang pt-BR", m["lang"] == "pt-BR", m["lang"])
            t("noindex (versão de trabalho)", m["noindex"])
            t("imagens com alt, width e height", all(i["alt"] and i["w"] and i["h"] for i in m["imgs"]), f"{len(m['imgs'])} img")
            t("sem âncora morta", not m["mortos"], m["mortos"] or "-")
            t("sem erro de JavaScript", not erros_js, erros_js[:2] or "-")
            if w < 800:
                baixos = [x for x in m["toque"] if x["h"] < 44]
                t("alvos de toque ≥ 44 px", not baixos, [f"{x['tag']} {x['h']}px {x['txt']!r}" for x in baixos][:5] or f"{len(m['toque'])} alvos")
            t("formulário presente", m["form"])
            t("honeypot site_url existe e está escondido de gente", m["hp"] and m["hpVisivel"] is False)
            for c in ("nome", "telefone", "email", "consentimento", "politica_versao", "utm_source", "utm_medium", "utm_campaign", "fbclid", "pagina", "site_url"):
                t(f"  campo {c}", c in m["campos"])
            pg.screenshot(path=os.path.join(AQUI, "capturas", f"{nome}.png"), full_page=True)

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
                    t("redirecionou para o Mercado Pago (link da pessoa)", "mercadopago.com" in pg.url, pg.url[:90])
            ctx.close()
        nav.close()
    print(f"\n{ok_n} ✅ · {ruim_n} 🔴")
    return 1 if ruim_n else 0


if __name__ == "__main__":
    sys.exit(main())
