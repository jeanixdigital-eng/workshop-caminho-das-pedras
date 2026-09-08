---
tipo: estrutura
frente: workshop
peça: página de venda do workshop (R$ 97, segunda 19/10/2026, ao vivo e online) + página de política de privacidade
criado: 2026-09-08
autor: Gael (mkt.site)
estado: PROPOSTA de estrutura para construir em staging. Publicar é ato do Jean (Alba → fila do Aprovador antes).
copy: rascunho/copy.md (Lia, 08/09) · texto da política: rascunho/privacidade-texto.md · prova: testes/medir.py
lido antes de decidir: cofre-workshop/20 Estratégia (Posicionamento, Tom de Voz, Persona Dr. Marcelo, Restrições de Conteúdo, Regras do CFO, Escada de Produtos) · 40 Peças/Dia 19 de outubro · 40 Peças/Duas agendas de 8 horas (direção de arte) · 60 Números/Os 5 Números da Clínica · 90 Fontes/02-diagnostico · jarvis-n8n-clinix/workshop/motores_wcp.py (porteiro `wcp/form/lead`, medido) · jarvis-site-clinix/.claude/skills (as seis) · jarvis-site-clinix/index.html (paleta e fontes da Clinix, para NÃO repetir)
---

# Página de venda do Workshop · estrutura e sistema de design

Este documento é para quem vai construir. Ele não contém copy: cada texto é referenciado pelo **nome do bloco em `copy.md`**. Onde a copy não tem um texto que a página precisa, está marcado como **lacuna para a Lia** (§9), não preenchido aqui.

**A decisão em cinco linhas.** A página é uma **conta feita em papel**: fundo cor de papel, tinta quase preta, **vermelho só no número ruim** (a única direção de arte que já existe para esta frente, no carrossel *Duas agendas de 8 horas*). Nenhuma cor da Clinix (navy + azul elétrico + âmbar) e nenhuma fonte dela. **Tipografia do sistema** (zero fonte carregada): a identidade aqui é o número com a origem declarada embaixo, não uma família tipográfica. Uma coluna só, 680 px, em todos os tamanhos: é um documento, lido no celular entre pacientes. **Um formulário, no fim**, com todos os botões apontando para ele por âncora e uma barra fixa de CTA no celular.

---

## 0. Arquivos e mapa

| Arquivo | O que é |
|---|---|
| `index.html` | a página de venda (HTML semântico, sem framework) |
| `privacidade.html` | a política de privacidade (§7) |
| `assets/estilo.css` | todo o CSS, compartilhado pelas duas páginas |
| `assets/pagina.js` | UTM/fbclid → campos escondidos · máscara de telefone · envio do formulário · barra fixa · carregador do pixel. Só o `index.html` usa |
| `assets/dieymisson.webp` + `assets/dieymisson.jpg` | a foto (§6). Hoje não existem; a página funciona sem elas |
| `assets/og.png` | imagem de compartilhamento 1200×630, tipográfica (papel + tinta), com o texto do **Title** do bloco META |

Âncoras internas (ids): `#topo` · `#para-quem` · `#a-conta` · `#o-que-acontece` · `#nao-vou-fazer` · `#quem-faz` · `#detalhes` · `#faq` · `#inscricao`. Todo botão CTA da página é `<a class="cta" href="#inscricao">` (a classe `cta` é o que o `medir.py` mede como alvo de toque).

Sem menu, sem header fixo, sem logo (não existe logo desta frente; não inventar um).

---

## 1. Ordem das seções e o trabalho de cada uma

A copy da Lia tem 13 blocos. A página tem **9 seções + rodapé**. Duas mudanças em relação à ordem da copy, com o porquê logo abaixo da tabela.

| # | Seção (id) | Bloco(s) da copy | Trabalho da seção | O que o Dr. Marcelo precisa sentir/saber para descer | Componentes |
|:-:|---|---|---|---|---|
| 0 | Header | linha `Dr. Dieymisson Mendes · CRO-MG [PENDENTE: número]` do bloco QUEM FAZ | dizer **quem é o "eu"** da headline para quem chega de anúncio sem ter visto o Reel; e cumprir o art. 4º da CFO-196 (nome + inscrição na publicação) | "é um dentista, com CRO" | texto pequeno em grafite; sem link |
| 1 | HERO (`#topo`) | HERO inteiro | continuar o Reel sem contradizer uma palavra: data, o que é, quanto custa. Botão à vista **sem rolar** | "é isso mesmo que o Reel prometeu; custa R$ 97; é dia 19" | h1 · parágrafo-lead · `cta` · microcopy |
| 2 | PARA QUEM (`#para-quem`) | PARA QUEM | reconhecimento, não convencimento: ele **já sabe que tem o problema** (persona). A parte "não é para você" é o filtro do iniciante e o primeiro sinal de honestidade | "essa frase é minha" | lista de **frases do dentista** (citação variante A) · h3 + parágrafo do "não é para você" |
| 3 | A CONTA (`#a-conta`) | A CONTA | **a prova**. É a resposta à objeção nº 8 ("mais um guru") antes de ela ser feita: número da clínica dele, com mês e origem declarados. Também é a **demonstração do formato**: mostrar uma conta feita vale mais que descrever o workshop | "ele mostra a conta dele mesmo, com número feio; isso eu nunca fiz na minha" | faixa `papel-2` · cards de número (§3.7) · parágrafos de origem · marcador PENDENTE D4 visível no topo da seção |
| 4 | O QUE ACONTECE NO DIA (`#o-que-acontece`) | O QUE ACONTECE NO DIA | o produto, concreto: os cinco números que **ele** vai levantar. Depois de ver a conta feita, a lista deixa de ser abstrata | "eu vou sair com esses cinco números; não é aula" | h2 = "Você não assiste. Você faz." · lista numerada seca (1 a 5) · caixa "o que ter por perto" |
| 5 | O QUE EU NÃO VOU FAZER (`#nao-vou-fazer`) | O QUE EU NÃO VOU FAZER | a recusa, que é o posicionamento inteiro. Trata as objeções "guru", "mentalidade" e a pressão de compra, de uma vez | "ele não vai me apressar nem me prometer nada" | citação variante B (a frase dos 35 %) · dois parágrafos |
| 6 | QUEM FAZ A CONTA COM VOCÊ (`#quem-faz`) | QUEM FAZ A CONTA COM VOCÊ | credencial **depois** da prova, não antes ("dono não precisa provar nada, ele mostra a clínica") | "tem clínica de verdade, no interior, como a minha" | citação variante B (frase do Posicionamento) · foto (§6) · parágrafos · linha nome + CRO |
| 7 | DETALHES (`#detalhes`) | DETALHES | logística que decide a compra: quando, quanto tempo, como chega o link, o que precisa ter | "cabe no meu dia; sei o que preciso ter" | `<dl>` |
| 8 | FAQ (`#faq`) | FAQ | as objeções restantes (interior, tempo, planilha, gravação, mentalidade), fechadas uma a uma | "não sobrou pergunta" | `<details>` × 6 |
| 9 | INSCRIÇÃO (`#inscricao`) | CTA FINAL + FORMULÁRIO | fechar e capturar. A headline do CTA FINAL, a frase-âncora e a microcopy **abrem** o formulário; o botão do bloco CTA FINAL **não entra** (apontaria para um formulário 200 px abaixo dele; o botão da seção é o `Ir para o pagamento`) | "é só nome, WhatsApp, e-mail; o pagamento vem em seguida" | faixa `papel-2` · h2 · citação B · formulário (§2) |
| 10 | Rodapé | RODAPÉ | identificação, aviso de que não promete resultado, quem vende, política, SAIR | | texto pequeno em grafite; links sublinhados |

**Por que A CONTA sobe para a 3ª posição (na copy ela é a 4ª).** A persona chega cética e o gancho do Reel é *"eu vou fazer a sua conta com você"*. A coisa mais forte que a página tem é a conta feita com número real e feio. Ela responde "mais um guru?" com evidência antes de qualquer descrição, e faz a lista dos cinco números (seção 4) ser lida como algo concreto. Se o D4 não aprovar a exposição dos números, a seção 3 sai inteira e a ordem continua de pé (HERO → PARA QUEM → O QUE ACONTECE...). Isso foi conferido: nenhuma seção depois dela depende de um número dela.

**Por que o botão do CTA FINAL sai.** Ver linha 9. Lia é avisada em §9.

### 1.1 Onde o formulário fica, e por quê

**Um formulário, no fim da página (seção 9). Todos os CTAs apontam para `#inscricao` por âncora. No celular, barra fixa de CTA no rodapé da tela.**

- **Não no topo.** Na tela de 390×844, um formulário de 4 campos + aceite + botão ocupa ~430 px: empurraria a headline e o lead para fora da dobra e transformaria a página numa tela de cadastro. Para quem chega cético, pedir WhatsApp antes de dizer qualquer coisa **é o padrão do guru** que a página existe para negar.
- **Não dois formulários.** Dois formulários são dois estados para sincronizar (erro, envio, sucesso, honeypot), dois lugares para a mesma prova no `medir.py`, e dividem a conversão em duas medidas que ninguém vai comparar com o tráfego que teremos. Um formulário com âncora entrega o mesmo caminho em um toque.
- **Quem já decidiu não paga pedágio:** o botão do hero está acima da dobra, e a barra fixa (§3.6) acompanha a rolagem no celular. Quem vem do Reel decidido toca o botão e chega ao formulário em um gesto; quem vem de anúncio frio lê até o fim e o formulário está onde a decisão termina.

### 1.2 A dobra (390×844 é a tela de projeto)

O que aparece **sem rolar** em 390×844, com a faixa de "versão de trabalho" ainda presente:

```
 0 ┌──────────────────────────────────────┐
   │ VERSÃO DE TRABALHO · n pendências     │  faixa amarela, 28 px (some na versão final)
28 ├──────────────────────────────────────┤
   │ Dr. Dieymisson Mendes · CRO-MG [PEND] │  header, 56 px, texto 14 px grafite
84 ├──────────────────────────────────────┤
   │                                       │  respiro 40 px
   │ Dia 19 de outubro eu vou             │  h1 ≈ 35 px, 3 linhas, line-height 1.08 ≈ 115 px
   │ fazer a sua conta com você.          │
   │                                       │  16 px
   │ Não é motivação e não é aula          │  lead 18 px, 5 linhas ≈ 130 px
   │ assistida. É um workshop ao vivo ...  │
   │                                       │  24 px
   │ ┌──────────────────────────────────┐ │
   │ │      Quero fazer a conta          │ │  botão 56 px, largura total
   │ └──────────────────────────────────┘ │
   │ Segunda, 19 de outubro de 2026 ·      │  microcopy 15 px grafite, 2 linhas
   │ R$ 97 · ao vivo e online              │
≈540├──────────────────────────────────────┤
   │ (respiro da seção)                    │
   │ É para você se uma destas frases      │  h2 da seção 2 aparece na borda inferior:
844└──────────────────────────────────────┘  é a deixa para rolar
```

Em **360×640** o mesmo bloco termina em ≈ 520 px: o botão continua acima da dobra. O hero **não** tem `min-height: 100vh`, de propósito: a seção seguinte precisa espiar na borda.

Em **1440×900** a coluna de 680 px fica centralizada, texto alinhado à esquerda, botão com largura automática (mín. 280 px); h1 em 56 px, 2 linhas. O resto da tela é papel vazio, e isso é a estética (espaço é o que separa "R$ 50k de R$ 5k" no `design-director.md`).

### 1.3 Títulos de seção (h2): de onde vem cada um

| Seção | h2 | Origem |
|---|---|---|
| 1 | *Dia 19 de outubro eu vou fazer a sua conta com você.* | HERO · headline (**é o h1**, único da página) |
| 2 | *É para você se uma destas frases é sua:* | PARA QUEM · primeira linha |
| 3 | *A conta* | nome do bloco, em caixa normal (Lia confirma) |
| 4 | *Você não assiste. Você faz.* | O QUE ACONTECE · primeira linha |
| 5 | *O que eu não vou fazer* | nome do bloco, em caixa normal (Lia confirma) |
| 6 | *Quem faz a conta com você* | nome do bloco (Lia confirma) |
| 7 | *Detalhes* | nome do bloco (Lia confirma) |
| 8 | *FAQ* | nome do bloco (Lia confirma; se quiser outro título, é copy dela) |
| 9 | *Segunda, 19 de outubro. A sua conta, feita com você.* | CTA FINAL · headline. O título do bloco FORMULÁRIO (*Deixa o seu contato. O pagamento vem em seguida.*) vira **h3** logo acima dos campos |

---

## 2. O formulário, especificado

`<form id="form-inscricao" method="post" action="https://n8n-webhook.clinixsystem.com.br/webhook/wcp/form/lead">` dentro da seção `#inscricao`. O `action` fica no HTML de propósito: sem JavaScript o formulário ainda posta (o servidor responde JSON cru, feio mas o lead entra). Com JavaScript, `pagina.js` intercepta o `submit`, faz `fetch` e trata a resposta.

### 2.1 Campos visíveis

Os textos entre aspas são do bloco FORMULÁRIO da copy. Eles entram como **`<label>` visível**, não como `placeholder`: placeholder some quando a pessoa digita, e no celular é o que faz alguém mandar o e-mail no campo do WhatsApp.

| `name` | tipo | label (copy) | `autocomplete` | teclado | obrigatório no servidor | altura |
|---|---|---|---|---|:-:|---|
| `nome` | `text` | "Seu nome" | `name` | `autocapitalize="words"` | sim (`NOME_OBRIGATORIO`) | 48 px |
| `telefone` | `tel` | "Seu WhatsApp, com DDD" | `tel-national` | `inputmode="tel"` · `maxlength="15"` | sim (`TELEFONE_INVALIDO` / `DDD_INVALIDO`) | 48 px |
| `email` | `email` | "Seu e-mail" | `email` | `inputmode="email"` · `autocapitalize="none"` · `spellcheck="false"` | sim (`EMAIL_INVALIDO`) | 48 px |
| `cidade` | `text` | "Cidade da clínica (opcional)" | `address-level2` | | não | 48 px |
| `consentimento` | `checkbox` `value="1"` | texto do "Consentimento" da copy, com *Política de Privacidade* como link para `privacidade.html` (`target="_blank" rel="noopener"`, para não perder o que já foi digitado) | | | sim (`SEM_CONSENTIMENTO`) | caixa 24 px dentro de um label com min-height 44 px |

`font-size` dos inputs **≥ 16 px** (iOS dá zoom automático abaixo disso e desloca a página). Nenhum `pattern`, nenhum `minlength`: a régua é do servidor (§2.6).

### 2.2 Campos escondidos (`type="hidden"`)

| `name` | valor | quem preenche |
|---|---|---|
| `politica_versao` | `2026-09-08` | fixo no HTML. **Tem de ser igual** à linha de versão no topo de `privacidade.html` (checklist §8) |
| `utm_source` · `utm_medium` · `utm_campaign` · `fbclid` | o parâmetro de mesmo nome da URL, ou vazio | `pagina.js` na carga |
| `pagina` | `location.href` sem a query (origem + caminho) | `pagina.js` na carga |

O servidor troca `utm_source` vazio por `formulario` e guarda `consent_versao` + `consent_em` no evento (medido em `motores_wcp.py`). A página não precisa mandar hora do aceite.

### 2.3 Campo-armadilha (`site_url`)

```html
<div class="hp" aria-hidden="true">
  <label for="site_url">Não preencha este campo</label>
  <input type="text" id="site_url" name="site_url" tabindex="-1" autocomplete="off">
</div>
```
```css
.hp { position: absolute; left: -10000px; top: auto; width: 1px; height: 1px; overflow: hidden; }
```

Fora da tela, não `display:none` (parte dos robôs pula campos com `display:none`; nenhum pula campo posicionado fora). O `medir.py` confere `left < 0` **ou** invisível, então qualquer uma das duas passa; a escolha é pelo robô, não pelo teste. O servidor responde `200 {"ok":true}` sem `next` a quem preencher (silêncio, para não ensinar o robô), portanto a página trata "sem `next`" como "recebido, sem redirecionar" (§2.5). O rótulo do campo é texto funcional, não copy; a Lia troca se quiser (§9).

### 2.4 Envio

Requisição **simples** de CORS (sem preflight): `application/x-www-form-urlencoded`, **nenhum header manual**, sem `credentials`. Header custom (`Content-Type: application/json`, `X-...`) dispararia um `OPTIONS` que o porteiro não foi provado a responder.

```js
form.noValidate = true;                                  // via JS: sem JS, o `required` nativo continua valendo
form.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  if (!validaLocal()) return;                            // só vazio e aceite (§2.6), com as mensagens da copy
  botao.disabled = true; botao.setAttribute('aria-busy', 'true');
  const ctrl = new AbortController(); const t = setTimeout(() => ctrl.abort(), 20000);
  try {
    const r = await fetch(form.action, { method: 'POST', body: new URLSearchParams(new FormData(form)), signal: ctrl.signal });
    let j = null; try { j = await r.json(); } catch (e) {}
    if (r.ok && j && j.ok === true) return sucesso(j.next);
    mostraErro((j && j.codigo) || (r.status === 429 ? 'MUITAS_TENTATIVAS' : 'FUNIL_INDISPONIVEL'));
  } catch (e) { mostraErro('FUNIL_INDISPONIVEL'); }
  finally { clearTimeout(t); botao.disabled = false; botao.removeAttribute('aria-busy'); }
});
```

- `new URLSearchParams(new FormData(form))` manda o checkbox só quando marcado (`consentimento=1`) e manda `site_url=` vazio: é exatamente o que o servidor e o `medir.py` esperam.
- Timeout de **20 s**: o porteiro chama o Barramento (com retry) e cria a preferência no Mercado Pago antes de responder; 10 s seria curto num 4G do interior.
- Clique duplo: botão desabilitado durante o envio; e o servidor deduplica por telefone + dia (`event_id`), então um reenvio não cria dois leads.

### 2.5 Respostas e o que a página faz

| Resposta | Página |
|---|---|
| `200 {"ok":true,"next":"https://..."}` | esconde o formulário; mostra a **mensagem de sucesso** da copy com `{primeiro nome}` = primeira palavra do campo `nome`, em `role="status"`; dispara `fbq('track','Lead')` se o pixel existir; **400 ms** depois `location.assign(next)`. Só redireciona se `next` começar com `https://` (defesa de uma linha contra `javascript:`). Deixa também um link com o texto do botão de envio ("Ir para o pagamento") apontando para `next`, porque navegador dentro do app do Instagram às vezes engole o redirecionamento |
| `200 {"ok":true}` sem `next` | esconde o formulário; mostra mensagem de "recebido" **que a copy ainda não tem** (§9). É o caminho do robô (armadilha) e do dia em que o Checkout e a config `LINK_CHECKOUT` falham ao mesmo tempo |
| `400 {"ok":false,"codigo":...}` | mensagem da copy **no campo** correspondente (tabela abaixo), `aria-invalid="true"` no campo, foco vai para ele |
| `429 MUITAS_TENTATIVAS` | mensagem da copy no bloco do formulário (não é de campo) |
| `502 FUNIL_INDISPONIVEL`, rede, timeout, JSON inválido, código desconhecido | mensagem "Funil indisponível" da copy, no bloco. O texto cita `@dieymisson_`: vira link para `https://www.instagram.com/dieymisson_/` (`target="_blank" rel="noopener"`) |

| `codigo` | campo que recebe a mensagem | mensagem (copy, bloco FORMULÁRIO) |
|---|---|---|
| `NOME_OBRIGATORIO` | `nome` | "Nome obrigatório" |
| `TELEFONE_INVALIDO` · `DDD_INVALIDO` | `telefone` | "Telefone inválido" (o mesmo texto para os dois; o servidor distingue, a copy não precisa) |
| `EMAIL_INVALIDO` | `email` | "E-mail inválido" |
| `SEM_CONSENTIMENTO` | `consentimento` | "Sem consentimento" |
| `MUITAS_TENTATIVAS` | bloco | "Muitas tentativas" |
| qualquer outro / falha | bloco | "Funil indisponível" |

Erro de campo: `<p class="campo-erro" id="erro-telefone">` logo abaixo do input, ligado por `aria-describedby`. Erro de bloco: `<div class="form-erro" role="alert">` acima do botão. Um erro novo apaga o anterior.

### 2.6 Validação no cliente: o que faz e o que não faz

**Faz:** recusa campo obrigatório vazio e aceite desmarcado, com as mensagens da copy (`NOME_OBRIGATORIO`, `TELEFONE_INVALIDO`, `EMAIL_INVALIDO`, `SEM_CONSENTIMENTO`), sem ir ao servidor. Vazio também é recusado pelo servidor, então nada que ele aceita é recusado aqui.

**Não faz:** não julga formato de telefone nem de e-mail. O servidor aceita **fixo de 10 dígitos** (`(38) 3821-1234`), celular de 11, celular antigo de 8 dígitos começando em 6 a 9 (ele insere o 9), número com `+55`/`55` na frente e com `0` de tronco. Uma regex "de celular" no cliente recusaria lead que o funil aceita.

### 2.7 Máscara de telefone (formatação, nunca recusa)

Espelha a normalização do `e164br` do servidor: só dígitos; tira `55` da frente quando o total é 12 ou 13; tira zeros à esquerda; corta em 11; formata `(DD) DDDDD-DDDD` com 11 e `(DD) DDDD-DDDD` com 10. O valor formatado é o que viaja; o servidor tira a pontuação.

```js
tel.addEventListener('input', () => {
  let d = tel.value.replace(/\D/g, '');
  if ((d.length === 12 || d.length === 13) && d.startsWith('55')) d = d.slice(2);
  d = d.replace(/^0+/, '').slice(0, 11);
  tel.value = d.length > 10 ? d.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3')
           : d.length > 6  ? d.replace(/^(\d{2})(\d{4})(\d{0,4}).*/,  '($1) $2-$3')
           : d.length > 2  ? d.replace(/^(\d{2})(\d{0,5})/, '($1) $2') : d;
});
```

### 2.8 Estados do botão de envio

| Estado | Aparência | Atributos |
|---|---|---|
| repouso | tinta, texto branco, "Ir para o pagamento" | |
| enviando | mesmo texto, opacidade 0,7, cursor `progress`, indicador de carga em CSS à esquerda do texto (anel de 16 px em borda, sem ícone) | `disabled` · `aria-busy="true"` |
| erro | volta ao repouso; a mensagem aparece no campo ou no bloco | `aria-invalid` no campo |
| sucesso | o formulário some; mensagem de sucesso + link para `next` | `role="status"` na mensagem |

Rótulo do botão **enquanto envia** não muda (a copy não tem esse texto; §9). O anel + `aria-busy` bastam para o olho e para o leitor de tela.

### 2.9 Acessibilidade do formulário

Labels visíveis ligados por `for`/`id`; erro por `aria-describedby`; `role="alert"` só para erro de bloco (assertivo) e `role="status"` para sucesso (educado); ordem de tabulação = ordem visual; honeypot com `tabindex="-1"` e `aria-hidden`; caixa de aceite nativa com `accent-color: var(--tinta)` (fica tinta nos navegadores modernos e continua operável em todos); link da política **antes** do botão (item 8.1 do plano de rastreio: a política é linkada e visível antes de enviar).

---

## 3. Sistema de design

### 3.1 Identidade: a decisão e o porquê

**Papel, tinta e vermelho.** A página parece uma conta armada numa folha: fundo cor de papel (não branco puro, não escuro), tinta quase preta, uma única cor a mais, o vermelho, reservada ao **número ruim** (faltas, dinheiro parado) e ao erro de formulário. Não há cor de "marca" no botão: o botão é tinta. É a leitura literal de *"Eu sou dentista, tenho clínica, e mostro a conta"*, e é a mesma direção do carrossel desta frente (*"fundo claro, tipografia grande e seca, sem ícone decorativo, sem stock photo. Vermelho só no número ruim."*), então o feed e a página vão parecer a mesma mão.

O que ela **não** é: não é o site da Clinix (navy `#050C1A`, azul `#4A7FFF`, glassmorphism, partículas, gradiente no título), não é o Instagram da Clinix (âmbar `#F4C025`, Montserrat), e não é o feed atual do `@dieymisson_` (identidade de dentista estético, que o diagnóstico mandou abandonar). Também não é o "dark premium" do `design-director.md`: aquele modo é o da Clinix; o que se aproveita dele aqui é o resto (espaço, hierarquia, um ponto focal por seção, nada de sombra óbvia, nada de ícone de enfeite).

### 3.2 Paleta (contraste calculado, WCAG)

| Token | Hex | Uso | Contraste medido |
|---|---|---|---|
| `--papel` | `#F6F3EC` | fundo da página | |
| `--papel-2` | `#EDE8DD` | faixa das seções 3 (A CONTA) e 9 (INSCRIÇÃO); caixa "o que ter por perto" | |
| `--branco` | `#FFFFFF` | superfície de card de número e de input | |
| `--tinta` | `#14120F` | texto principal, títulos, números, botão | sobre papel **16,87:1** · sobre branco 18,70:1 · sobre papel-2 15,30:1 |
| `--tinta-2` | `#2B2823` | hover do botão | branco sobre ela **14,68:1** |
| `--grafite` | `#4A4741` | texto secundário: header, microcopy, origem dos números, rodapé, rótulos dos cards | sobre papel **8,35:1** · sobre branco 9,26:1 · sobre papel-2 7,58:1 |
| `--vermelho` | `#B42318` | **só** o número ruim e texto de erro | sobre papel **5,93:1** · sobre branco 6,57:1 · sobre papel-2 5,38:1 · sobre erro-fundo 5,65:1 |
| `--erro-fundo` | `#FBEAE8` | fundo do erro de bloco | tinta sobre ela 16,06:1 |
| `--borda` | `#8A847A` | borda de input (1 px) | sobre branco **3,71:1** (≥ 3:1 exigido para componente) |
| `--linha` | `#D9D4C9` | divisórias decorativas, borda de card | decorativa, sem exigência |
| `--pendente` | `#FFE45C` | fundo do marcador `[PENDENTE]` e da faixa "versão de trabalho" | tinta sobre ela **14,69:1** |
| Botão | branco sobre `--tinta` | | **18,70:1** |

Tudo acima de AA (4,5:1 para texto; 3:1 para componente). O vermelho **nunca** vira botão nem link: se virasse, "vermelho = número ruim" deixaria de significar alguma coisa. Sem gradiente, sem sombra, sem borda translúcida.

Regra de uso do vermelho, para quem constrói: ele aparece em **exatamente quatro** números da página (84, R$ 3.472,56, 490, R$ 394.249,81) e nas mensagens de erro. Em mais nada.

### 3.3 Tipografia: sistema, sem fonte carregada

```css
font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

Por quê, e não uma fonte do Google:

1. **A pessoa lê no celular, entre pacientes, no interior.** Zero byte de fonte, zero troca de fonte no meio da leitura (FOUT), zero deslocamento de layout. O texto do h1 é o LCP e aparece no primeiro frame.
2. **A política de privacidade lista os fornecedores que recebem dado** (Mercado Pago, GHL, servidor, Meta, GitHub Pages). Carregar fonte do CDN do Google manda o IP do visitante para mais um fornecedor que a política não cita. Ou entraria na lista, ou a fonte sai. A fonte saiu.
3. **A identidade não está na fonte.** O Reel é "texto na tela", a direção do carrossel é "tipografia grande e seca". SF (iPhone), Roboto (Android) e Segoe (Windows) em 700, grandes, com tracking negativo, são exatamente isso. `font-variant-numeric: tabular-nums` entra como melhoria progressiva (SF e Roboto têm o recurso; Segoe não foi medido aqui): os números da seção A CONTA ficam um por linha, não em coluna alinhada, então nada depende dele.
4. Se um dia os sócios quiserem a mesma face do carrossel na página, o caminho é **auto-hospedar** dois pesos em `assets/fonts/` (OFL permite), não o CDN. Fica anotado, não feito.

Pesos: **400** e **700** só (Roboto não tem 800 garantido em Android antigo). Sem itálico (SF e Roboto itálicos parecem "inclinado"; a citação se marca por tamanho e régua, não por itálico).

### 3.4 Escala tipográfica (`clamp()`, 390 px → 1440 px)

| Token | `clamp()` | 390 px | 1440 px | Onde |
|---|---|---|---|---|
| `--t-h1` | `clamp(2.125rem, 1.4rem + 3.2vw, 3.5rem)` | 35 px | 56 px | h1 · line-height 1.08 · letter-spacing −0.02em · 700 |
| `--t-num` | `clamp(2.5rem, 1.5rem + 5vw, 5rem)` | 44 px | 80 px | os números-resultado (R$ 41,34 e os dois vermelhos em R$) · line-height 1 · −0.02em · 700 · `tabular-nums` |
| `--t-num-2` | `clamp(1.75rem, 1.2rem + 2.4vw, 2.75rem)` | 28 px | 44 px | os números de entrada (R$ 40.844 · 988 · 84 · 490) |
| `--t-h2` | `clamp(1.5rem, 1.1rem + 1.8vw, 2.25rem)` | 25 px | 36 px | h2 · line-height 1.15 · −0.015em · 700 |
| `--t-h3` | `clamp(1.125rem, 1rem + 0.6vw, 1.375rem)` | 18 px | 22 px | h3, título do card, pergunta do FAQ · 700 |
| `--t-lead` | `clamp(1.125rem, 1rem + 0.6vw, 1.375rem)` | 18 px | 22 px | subheadline do hero, frases do dentista (citação A) · line-height 1.45 |
| `--t-cit` | `clamp(1.25rem, 1.05rem + 1.2vw, 1.75rem)` | 21 px | 28 px | citação B (frases-âncora) · line-height 1.3 · 700 |
| `--t-corpo` | `clamp(1rem, 0.95rem + 0.3vw, 1.125rem)` | 16 px | 18 px | parágrafos · line-height 1.6 · max-width 65ch |
| `--t-peq` | `0.9375rem` | 15 px | 15 px | microcopy, origem dos números, rodapé, mensagens de erro |
| `--t-min` | `0.875rem` | 14 px | 14 px | header, rótulo de card (caixa alta, letter-spacing 0.06em). **Nada abaixo de 14 px** |

Máximo de três tamanhos por seção (regra do `design-director.md`): na seção 3 são `--t-num`, `--t-num-2` e `--t-peq` (a origem), com o h2 fora dessa conta.

### 3.5 Espaçamento e grade

- Escala de 8: `--e1` 8 · `--e2` 16 · `--e3` 24 · `--e4` 32 · `--e5` 48 · `--e6` 64.
- Seção: `padding: clamp(56px, 8vw, 112px) 0`. Entre h2 e o primeiro conteúdo: `--e4`. Entre parágrafos: `--e2`.
- Contêiner: `max-width: 680px; margin: 0 auto; padding: 0 clamp(20px, 5vw, 40px)`. Em 390 px o texto tem 350 px de largura; em 1440 a coluna fica no centro. **Uma coluna em todos os tamanhos** (a única exceção é a seção 6, foto ao lado do texto a partir de 768 px).
- Breakpoints: base = celular; `min-width: 768px` (botão com largura automática, foto ao lado, barra fixa some); `min-width: 1024px` (só respiro maior). Dois, não quatro.
- Raio de canto: 8 px em botão e input, 12 px em card, 4 px no marcador PENDENTE. Não é tudo igual, e não passa disso.

### 3.6 Componentes

**Botão CTA (`.cta`, também o `<button type="submit">`)**
```css
.cta { display:flex; align-items:center; justify-content:center; gap:10px; width:100%; min-height:56px;
       padding:0 24px; background:var(--tinta); color:#fff; font-size:1.0625rem; font-weight:700;
       border:0; border-radius:8px; text-decoration:none; transition:background-color .15s ease, transform .1s ease; }
.cta:hover { background:var(--tinta-2); }
.cta:active { transform:translateY(1px); }
.cta:focus-visible { outline:3px solid var(--tinta); outline-offset:3px; }
@media (min-width:768px) { .cta { width:auto; min-width:280px; } }
```
Altura 56 no celular (o `cro-expert.md` pede 52 mínimo; o `medir.py` exige 44). Um só estilo de botão na página inteira: não existe "secundário".

**Card de número (`.num`)**: superfície branca, borda 1 px `--linha`, raio 12, padding 20/24. Dentro, três linhas: rótulo (`--t-min`, caixa alta, grafite), número (`--t-num-2` ou `--t-num`, tinta ou vermelho), e a **origem** (`--t-peq`, grafite). Sem ícone, sem sombra, sem hover (não é clicável). O card **não anima**: o contador que sobe do `ui-components.md` não entra; número que "sobe" é teatro, e o número aqui é fato.

**Citação, duas variantes**
- **A, a frase do dentista** (PARA QUEM): o texto entre aspas como está na copy, `--t-lead`, tinta, 400, uma por linha de lista (`<ul>` sem marcador), separadas por `--e3`. Sem régua, sem aspas gráficas gigantes: as aspas são as do texto.
- **B, a frase-âncora** (as três frases do Dr. Dieymisson: a dos 35 %, a do Posicionamento, a do CTA FINAL): `<blockquote>`, `--t-cit`, 700, régua de 4 px em `--tinta` à esquerda, padding-left `--e3`. É o único elemento gráfico da página além dos cards.

**Lista numerada seca** (os cinco números, seção 4): `<ol>` com o numeral em `--t-h2` 700 tinta à esquerda (coluna de 2.5rem), título em `--t-h3` 700 e descrição em `--t-corpo`. Numeral é texto, não ícone.

**Detalhes** (seção 7): `<dl>`; `dt` em `--t-min` caixa alta grafite, `dd` em `--t-corpo` tinta; divisória `--linha` entre pares; a partir de 768 px `dt` e `dd` na mesma linha (grid `10rem 1fr`).

**FAQ** (seção 8): `<details>` por pergunta; `<summary>` contém um `<h3>` com a pergunta; `min-height: 48px`; marcador nativo removido e um `+` em texto à direita, que vira `−` quando aberto (`details[open] summary::after { content: "−" }`). Todos fechados de início, vários podem ficar abertos (sem o atributo `name`). A resposta em `--t-corpo`, padding `--e2` `--e4`.

**Barra fixa de CTA no celular: sim.** A página tem nove seções e o formulário está no fim; quem decide no meio (tipicamente ao ver A CONTA) não pode ter de rolar cinco telas. Especificação: `position: fixed; bottom: 0`, fundo `--papel`, borda superior 1 px `--linha`, padding 8 px 16 px + `env(safe-area-inset-bottom)`, dentro dela um `.cta` de 52 px com o texto do botão do HERO ("Quero fazer a conta") e `href="#inscricao"`. Só existe abaixo de 768 px. **Aparece** quando o botão do hero sai da tela (IntersectionObserver no `#cta-hero`) e **some** enquanto a seção `#inscricao` está visível (senão cobre o botão de envio e briga com o teclado). Enquanto a barra existe, `body { padding-bottom: 80px }` para o rodapé não ficar embaixo dela. Sem animação de entrada além de `opacity .15s`.

**Marcador `[PENDENTE]`**: `<mark class="pendente">PENDENTE: texto da copy</mark>`, fundo `--pendente`, tinta, 600, padding 2 px 6 px, raio 4. Fica **no lugar exato do texto que falta** (o número do CRO, o horário, a duração...) e, no caso do D4, no topo da seção 3, em linha própria. A faixa de topo `VERSÃO DE TRABALHO · n pendências` (`role="note"`, mesmo amarelo) conta os `.pendente` por JS. Para publicar: remover cada `<mark>` (o conteúdo dele é nota, nunca texto) e a faixa; `grep -c 'class="pendente"' index.html privacidade.html` tem de dar **0** (checklist §8). Nada de `display:none` por classe para "esconder na final": marcador escondido é marcador esquecido.

**Input**: 48 px, borda 1 px `--borda`, fundo branco, raio 8, padding 0 14 px, `font-size: 1rem`; foco: borda 2 px `--tinta` + `outline: 3px solid var(--tinta); outline-offset: 2px`; erro: borda 2 px `--vermelho`.

**Caixa "o que ter por perto"** (fim da seção 4): `--papel-2`, raio 12, padding `--e3`, sem borda. Texto da copy inteiro.

### 3.7 A seção A CONTA: como mostrar uma conta feita

Regra geral: **o parágrafo da copy fica inteiro, embaixo do card**, como origem. O card só destaca o número e o rótulo que o próprio parágrafo usa. Nada é reescrito; nada é gráfico.

```
[PENDENTE: aprovação D4 ...]                          ← mark, linha própria, no topo

h2  A conta
h3  A hora clínica, em três linhas:                   ← as três linhas da copy, como <ol> simples

h3  Na minha clínica, agosto de 2026:

┌ card ───────────────────────────────┐
│ CUSTO FIXO DO MÊS                    │  rótulo (--t-min)
│ R$ 40.844                            │  --t-num-2, tinta
└──────────────────────────────────────┘
        ÷                                   operador em --t-h2 grafite, centralizado (a copy usa "÷")
┌ card ───────────────────────────────┐
│ HORAS DE CADEIRA NO MÊS              │
│ 988                                  │  --t-num-2
│ (parágrafo da copy: "São 4 cadeiras, │  origem, --t-peq grafite
│  9 horas e meia por dia, 26 dias..." │
│  ... número chutado.")               │
└──────────────────────────────────────┘
        =
┌ card ───────────────────────────────┐
│ POR HORA DE CADEIRA                  │
│ R$ 41,34                             │  --t-num, tinta (o maior número preto da página)
│ "R$ 40.844 ÷ 988 horas = R$ 41,34    │  a frase da copy, inteira
│  por hora de cadeira. Vazia ou       │
│  ocupada, ela custou isso."          │
└──────────────────────────────────────┘

h3  Agora os dois números que quase ninguém põe na frente da hora clínica:

┌ card ───────────────────────────────┐
│ FALTAS EM AGOSTO                     │
│ 84                                   │  --t-num-2, VERMELHO
│ 84 × R$ 41,34 =                      │  --t-peq grafite
│ R$ 3.472,56                          │  --t-num, VERMELHO
│ (parágrafo da copy inteiro:          │
│  "Contadas na agenda ... para        │
│  ninguém sentar.")                   │
└──────────────────────────────────────┘
┌ card ───────────────────────────────┐
│ ORÇAMENTOS NÃO APROVADOS, AGOSTO     │
│ 490                                  │  --t-num-2, VERMELHO
│ R$ 394.249,81                        │  --t-num, VERMELHO
│ (parágrafo da copy inteiro)          │
└──────────────────────────────────────┘

p   "Essa é a versão simples da conta. ..."          ← último parágrafo da copy, --t-corpo
```

O que **não** entra, e por quê: gráfico de barra (compararia números de natureza diferente e insinuaria proporção que a copy não afirma), porcentagem (a marca recusa percentual), contador animado, "e na sua clínica?" com campo para o leitor digitar (é o workshop, não a página), qualquer projeção. Os operadores `÷`, `=`, `×` são os da própria copy. Os rótulos dos cards são palavras da copy, em caixa alta por CSS (`text-transform`), não retextualizados.

Os números da tela têm de bater com `copy.md` **e** com `60 Números/Os 5 Números da Clínica.md` (a conta 40.844 ÷ 988 = 41,34 e 84 × 41,34 = 3.472,56 foram reconferidas aqui). Se o Dr. Dieymisson mudar um número no D4, mudam os três lugares.

### 3.8 Animação

Quase nenhuma, de propósito: quem lê entre pacientes não espera "reveal". O que existe: transição de cor e o `translateY(1px)` do botão, `opacity` da barra fixa, abertura nativa do `<details>`. `html { scroll-behavior: smooth }` só sob `prefers-reduced-motion: no-preference`. E:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition: none !important; animation: none !important; }
  html { scroll-behavior: auto; }
}
```

Nada de GSAP, Lenis, ScrollTrigger, partículas ou ApexCharts (as bibliotecas do `animation.md` e do `ui-components.md` são do site da Clinix e estourariam o orçamento de 60 KB sozinhas).

---

## 4. Orçamento de desempenho e acessibilidade

| Item | Teto | Como medir |
|---|---|---|
| `assets/estilo.css` + `assets/pagina.js` | **≤ 60 KB** somados, sem minificar (alvo: CSS ≤ 20 KB, JS ≤ 8 KB) | `wc -c assets/estilo.css assets/pagina.js` |
| `index.html` | ≤ 40 KB | `wc -c` |
| Fontes carregadas | **0** (§3.3) | painel de rede: nenhuma requisição a `fonts.*` |
| Requisições de terceiro com `data-pixel-id=""` | **0** | painel de rede: nada para `facebook.*`, `google*`, CDN algum |
| Foto | ≤ 120 KB (webp) + ≤ 200 KB (jpg de reserva), `width`/`height` no HTML, `loading="lazy"`, `decoding="async"` | `ls -l assets/` + `medir.py` |
| `og.png` | ≤ 200 KB, 1200×630 | |
| Framework / build | nenhum | |
| LCP no celular | o h1 (texto). Sem imagem acima da dobra | Lighthouse mobile, se disponível |
| CLS | 0: espaço da foto reservado por `width/height`; barra fixa não desloca conteúdo (`padding-bottom` estático) | |

**`<head>` (versão de trabalho):**
```html
<!doctype html><html lang="pt-BR">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">      <!-- sem maximum-scale: zoom é acessibilidade -->
<title>[META · Title]</title>
<meta name="description" content="[META · Description]">
<meta name="robots" content="noindex,nofollow">                            <!-- versão de trabalho -->
<!-- <link rel="canonical" href=""> — só entra quando o domínio existir; canonical vazio resolveria para a URL do github.io, que não é o endereço final -->
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="[META · Title]">
<meta property="og:description" content="[META · Description]">
<meta property="og:image" content="[URL ABSOLUTA de assets/og.png — pendente do endereço; WhatsApp não lê caminho relativo]">
<meta property="og:url" content="[pendente do endereço]">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F6F3EC">
<link rel="stylesheet" href="assets/estilo.css">
<script src="assets/pagina.js" defer></script>
```

**Acessibilidade (requisito, não auditoria depois):**
- Um `<h1>` (a headline do HERO); cada seção é `<section aria-labelledby="...">` com seu `<h2>`; `header`, `main`, `footer` como landmarks; link "pular para o conteúdo" como primeiro elemento focável (texto funcional, §9).
- Foco visível em tudo que é focável (outline 3 px tinta, offset 2 a 3 px; nunca `outline: none` sem substituto).
- Cor não é o único sinal: o número vermelho vem com o rótulo em texto ("faltas", "não aprovados"); o erro vem com texto e `aria-invalid`.
- Alvos de toque ≥ 44 px (botões 56, inputs 48, `summary` 48, links do rodapé com padding vertical 12 px, label do aceite 44).
- `<details>` funciona por teclado nativamente; não substituir por div + JS.
- Imagem com `alt` (§6); OG não precisa.
- Texto redimensionável até 200 % sem estouro horizontal (é o que `clamp()` com `rem` garante; conferir em §8).
- `lang="pt-BR"` no `<html>` das duas páginas.

---

## 5. Rastreio

**Pixel da Meta, carregado só se houver id.** O id fica em `<body data-pixel-id="">` (hoje vazio: a conta de anúncios tem **0 pixels**, medido em 04/09). O carregador vive no fim de `pagina.js`:

```js
(function () {
  var id = document.body.dataset.pixelId;
  if (!id) return;                                   // hoje: nenhuma requisição sai daqui
  /* código-base oficial do pixel (fbevents.js), sem alteração */
  fbq('init', id); fbq('track', 'PageView');
})();
```

- Evento **`Lead`** no sucesso do formulário (§2.5), antes do redirecionamento, com 400 ms de folga para a requisição do pixel sair. Parâmetros do evento: os que o **Igor** definir; por padrão só o nome do evento.
- `InitiateCheckout` e `Purchase` **não** são desta página (o primeiro é do checkout do Mercado Pago; o segundo é do servidor, via `WCP · Meta`, com dedupe pelo id da transação).
- O `<noscript>` com a imagem do pixel só entra no HTML **quando** o id existir (não dá para deixá-lo condicional).
- **Decisão em aberto que não é minha:** a política (§8 do texto-base) diz que ainda não se decidiu se o pixel pede aceite antes de carregar. Enquanto o id está vazio não há o que condicionar. No dia em que o id entrar, o carregador acima é o único lugar a mudar: ou carrega direto, ou passa a depender de um aceite. Estrutura pronta para os dois; decisão do Jean com a Alba.

**UTM e fbclid** (§2.2): lidos de `location.search` na carga, gravados nos campos escondidos; `pagina` = URL sem query. Nada em cookie, nada em `localStorage`: se a pessoa recarregar sem os parâmetros, eles se perdem, e isso é aceitável (o servidor registra `utm_source=formulario`).

**Sem GA4.** Nenhum outro script de terceiro.

---

## 6. Foto do Dr. Dieymisson

**Slot** (seção 6): `<picture>` com `assets/dieymisson.webp` e `assets/dieymisson.jpg`, proporção **4:5** (retrato), entregue em **800×1000 px** (`width="800" height="1000"`), `loading="lazy"`, `decoding="async"`, raio 12. No celular ocupa a largura da coluna (máx. 320 px, centralizada à esquerda); a partir de 768 px fica à esquerda em 40 % da coluna com o texto ao lado. `alt`: texto a pedir à Lia (§9); enquanto não vier, `alt="Dr. Dieymisson Mendes"`.

**O que pedir a ele** (um pedido só, para não gastar um dia de câmera dele):
- Retrato **vertical**, original com ≥ 1600×2000 px, sem filtro, sem recorte apertado.
- Na clínica, **sentado à mesa com o computador** (é o enquadramento do Reel *Dia 19 de outubro*: quem vem do vídeo reconhece o lugar). Nenhuma tela com nome de paciente legível, nenhum paciente ao fundo (Regras do CFO, achado 1).
- Luz de janela, olhando para a câmera, expressão neutra: sem sorriso de banner, sem braço cruzado de palestrante. Roupa de trabalho (jaleco ou scrub): é a credencial *"tenho clínica"* em tempo presente.
- Fundo real da clínica, nada de stock nem estúdio.

**Fallback digno sem foto:** o slot **não existe no DOM** (nem `<picture>` vazia, nem silhueta cinza, nem monograma: os três gritam "faltou a foto"). A seção 6 vira uma coluna só: a citação B do Posicionamento no topo, os parágrafos, e a linha nome + CRO em `--t-h3` 700 com uma régua de 1 px `--linha` acima. Assim a página é publicável sem a foto e ganha com ela, sem depender dela.

---

## 7. Página de privacidade (`privacidade.html`)

Mesmo CSS, mesmo header e rodapé, `noindex,nofollow`, `lang="pt-BR"`, `<title>` = "Política de Privacidade · " + o Title do META (a Lia confirma). Sem JavaScript.

Estrutura, a partir de `privacidade-texto.md`:

```
header   (a mesma linha nome · CRO)
main.container (max-width 680px; medida de texto 65ch)
  h1  Política de Privacidade
  p.versao   "Workshop de 19 de outubro · versão 2026-09-08"    ← a string da versão TEM de ser igual ao hidden politica_versao
  p   "Aplica-se a ..."
  nav[aria-label] > ol   os 12 títulos numerados, como links de âncora (#s1 ... #s12): no celular é o índice; são 12 seções
  section#s1 > h2 "1. Quem é responsável pelos seus dados" ... até section#s12
    - tabelas (2.1 e 5): <table> com <th scope="col">; abaixo de 640 px viram linhas empilhadas
      (tr → bloco; td::before { content: attr(data-label) } em --t-min caixa alta grafite), sem rolagem horizontal
    - listas numeradas do item 3 como <ol>
    - e-mail do item 9 como link mailto:
    - marcadores [PENDENTE] com o mesmo <mark class="pendente"> da página
  p   link de volta para index.html (texto funcional, §9)
footer   (o mesmo rodapé)
```

Estilo: `--t-corpo` a 17 px no celular (`clamp(1.0625rem, ..., 1.125rem)`), h2 em `--t-h3`+2 px (1.375rem), espaçamento entre seções `--e5`. Sem cards, sem faixa: é um documento para ler. A página existe para responder HTTP 200 no link do aceite (item 8.1) e para a Alba carimbar; nada nela é decorativo.

---

## 8. Checklist de verificação (aprovar a página construída)

**Automático (repo):**
- [ ] `python3 testes/medir.py` → tudo ✅ em 360×640, 390×844 e 1440×900: sem estouro horizontal, um h1, `lang`, `noindex`, imagens com `alt`/`width`/`height`, sem âncora morta, sem erro de JS, toque ≥ 44 px, honeypot escondido, os 11 campos presentes.
- [ ] `python3 testes/medir.py --simular` → POST leva `consentimento=1`, `politica_versao=`, `utm_*`, `fbclid`, `pagina`; `site_url` vazio; redirecionou para `next`.
- [ ] `python3 testes/medir.py --enviar` (telefone da faixa de teste) → chega ao Mercado Pago. Depois: `python3 ~/jarvis-n8n-clinix/workshop/testes/injetar_evento.py --limpar --host n8n.clinixsystem.com.br` e o contato de teste removido do GHL (**o Jean remove**; registrar quem e quando).
- [ ] `wc -c assets/estilo.css assets/pagina.js` → soma ≤ 61 440 bytes. `wc -c index.html` ≤ 40 KB.
- [ ] `grep -c 'class="pendente"' index.html privacidade.html` → na versão de trabalho, igual ao número de pendências da copy + as da política; **na versão final, 0**.
- [ ] `grep -o 'politica_versao" value="[^"]*"' index.html` e a linha de versão em `privacidade.html` → a mesma string.
- [ ] Contraste: rodar os pares de §3.2 num script (fórmula WCAG); nenhum texto < 4,5:1, borda de input ≥ 3:1.
- [ ] Texto da página = texto de `copy.md`, bloco a bloco (extrair `innerText` e comparar; Lia/Alba fazem a leitura final). Os cinco números iguais aos de `Os 5 Números da Clínica.md`.

**No navegador (DevTools, painel de rede):**
- [ ] Com `data-pixel-id=""`: **zero** requisição para `facebook.*`/`connect.facebook.net`; zero para `fonts.googleapis`/`gstatic`; zero para qualquer CDN.
- [ ] CORS: `curl -si -X POST -H "Origin: https://ORIGEM-DA-PAGINA" https://n8n-webhook.clinixsystem.com.br/webhook/wcp/form/lead --data-urlencode nome=X` → cabeçalho `access-control-allow-origin` presente. Hoje `ORIGENS_FORMULARIO` no porteiro está vazio (tudo passa); quando o Jean restringir, **remedir** a partir do endereço real da página.
- [ ] Sem JS (desligar em DevTools): o formulário ainda posta pelo `action`, o `required` nativo segura vazio e aceite desmarcado.
- [ ] `prefers-reduced-motion: reduce` emulado: nenhuma transição, rolagem sem `smooth`.
- [ ] Zoom de texto a 200 %: sem estouro horizontal, nada sobreposto.
- [ ] Teclado só: Tab percorre header → hero CTA → ... → campos → aceite → botão → rodapé; foco visível em cada parada; `<details>` abre com Enter/Espaço; honeypot nunca recebe foco.
- [ ] Leitor de tela (VoiceOver/TalkBack, passada rápida): labels lidos com os campos; erro anunciado; sucesso anunciado; landmarks presentes.
- [ ] Links: `privacidade.html` responde (200 no servidor, abre em `file://`); link do Instagram abre em nova aba; todas as âncoras têm alvo (o `medir.py` já cobre); nenhum `href="#"` solto.

**Em aparelho real (os dois que a persona usa):**
- [ ] iPhone/Safari: teclado numérico no WhatsApp; ao focar um campo a barra fixa **não** aparece por cima do teclado nem do botão; nenhum zoom automático ao focar (fonte ≥ 16 px); o redirecionamento para o Mercado Pago funciona dentro do navegador do Instagram.
- [ ] Android/Chrome: autopreenchimento de contato **não** preenche `site_url` (abrir o formulário, aceitar a sugestão de preenchimento, conferir que o envio não cai no silêncio); máscara formata ao colar `+55 38 9...`.
- [ ] 360 px: microcopy do hero e rótulos dos cards sem quebra feia; os números vermelhos em `R$ 394.249,81` cabem em uma linha (senão reduzir `--t-num` no mínimo do `clamp`, nunca quebrar o número).

**Antes de publicar (fora do meu escopo, listado para ninguém esquecer):**
- [ ] Carimbo da Alba na página e na política; aprovação do Jean registrada; caminho de volta escrito.
- [ ] Trocar `noindex,nofollow` só quando o Jean mandar; `og:image`/`og:url` com URL absoluta do endereço final; testar a prévia no WhatsApp (mandar o link para si mesmo).
- [ ] `data-pixel-id` continua vazio até o Igor entregar o id e a decisão do aceite (§5).

---

## 9. O que falta e não é meu

**Lia (copy):** (1) mensagem para `ok:true` **sem** `next` ("recebi, o link chega no seu WhatsApp", ou o que ela decidir); (2) rótulo do botão enquanto envia, se quiser um; (3) rótulo do campo-armadilha (hoje "Não preencha este campo"); (4) texto do link "pular para o conteúdo" e do link de volta na política; (5) texto do `alt` da foto; (6) confirmar os h2 de nome de bloco (§1.3) e o título da página de privacidade; (7) ciência de que o **botão do CTA FINAL não entra** (§1, linha 9) e de que os rótulos dos cards da seção A CONTA são palavras da própria copy em caixa alta por CSS.

**Igor (rastreio):** parâmetros do evento `Lead`; o id do pixel quando existir; a convenção de UTM que o Rui vai usar nos anúncios (a página captura qualquer valor, mas alguém precisa decidir os nomes).

**Jean:** endereço da página (destrava `og:url`, `og:image`, canonical e o CORS restrito no porteiro); decisão do aceite antes do pixel, com a Alba; CNPJ/razão social do vendedor (pendência 6 da copy e §1 da política); remoção dos contatos de teste no GHL após o `--enviar`.

**Dr. Dieymisson:** D4 (expor os números; sem ele a seção 3 sai inteira), CRO, horário, duração, a foto (§6).

**Bruno:** gravação (pendência 5 da copy), quem olha o direct a partir de 18/09 (pendência 9).

**Alba:** carimbo das duas páginas. Eu não carimbo a própria conformidade.
