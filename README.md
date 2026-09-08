# Página de venda do Workshop (frente `@dieymisson_`)

Página estática (HTML + CSS + JS, sem build) que vende o workshop de R$ 97 de 19/10/2026.
Nasceu em 08/09/2026 a pedido do Jean. **Frente Workshop**, nunca a Clinix System.

- Formulário posta no porteiro `wcp/form/lead` do n8n da Clinix (que devolve o link de pagamento da pessoa).
- **O pagamento acontece aqui dentro** (`checkout.html`, Payment Brick do Mercado Pago; confirmação em
  `obrigado.html`). A página lê a sessão em `wcp/checkout/sessao?c=<token>` e cria a cobrança em
  `wcp/pagamento/criar`. Nenhum preço fica escrito no HTML: o valor da tela vem sempre do servidor.
- Estratégia e decisões vivem no cofre `cofre-workshop` (`50 Tarefas/Funil em GHL + n8n.md`).
- `rascunho/` guarda a copy (Lia) e a estrutura (Gael) que geraram a página.
- ⛔ Aqui não entra segredo, PII, dado de cliente. Nenhum número de paciente.

## O sistema visual (reconstruído em 08/09/2026)

**O que é.** A base é o **Nocturne** (`nocturne/styles.css`, cópia de leitura do
Claude Design, ⛔ não se edita). O que evoluímos vive só em `assets/estilo.css`, com
o porquê escrito ao lado de cada adição: um chão mais escuro para as seções de
quebra (`--fundo-baixo`), a tinta de capacidade das ilustrações
(`--tinta-capacidade`) e uma família de display, a **Newsreader**, hospedada em
`assets/fontes/` e subsetada por nós (53,8 KB). ⛔ Nunca CDN de fonte: a política
de privacidade lista quem recebe dado do visitante.

**Como o dado vira desenho.** Toda ilustração é SVG inline escrito à mão, e a
tinta é regra: acento = a conta que a gente faz, `--tinta-capacidade` = o que a
clínica tem, `--ruim` = o que escorreu. Todo número desenhado é de **agosto de
2026, da clínica do Dr. Dieymisson**, com o mês declarado na legenda. A grade de
orçamentos é um `<pattern>` de 35 × 14 que dá **490 pontos exatos**, e o teste
confere essa multiplicação. Os objetos tridimensionais (`assets/img/`) foram
gerados por IA e são **objetos, nunca pessoas**: não existe foto do
Dr. Dieymisson no acervo, e o que pedir a ele está em `rascunho/fotos-pedidas.md`.

**Como foi testado.** `python3 testes/medir.py --simular` (107 asserções) e
`python3 testes/medir_checkout.py` (160), os dois em 0 🔴. Além do que já media,
o primeiro agora prova que toda imagem carregou de verdade, que nenhuma
ilustração está colapsada, que a grade tem 490 pontos, que **o número pintado na
tela é igual ao `data-conta` dele**, o contraste AA calculado em 9 papéis de texto
e zero travessão nos arquivos da página.

**O que não repetir.** Três armadilhas, todas custaram tempo em 08/09:
1. **`scale(0)` esconde igual a `opacity: 0`.** Animação de entrada tem de ter o
   estado FINAL no repouso e a entrada por `@keyframes`, senão o bloco some quando
   o `IntersectionObserver` não dispara.
2. **`full_page=True` do Chromium não pinta imagem que nunca esteve no viewport.**
   A captura sai com buraco e parece defeito de página. O teste rola, estica o
   viewport até a altura do documento e só então fotografa.
3. **Contador animado pode congelar num valor intermediário** (a aba vai para
   segundo plano e o `requestAnimationFrame` para). Numa página que vende "os
   números são os reais da minha clínica", número errado na tela é defeito de
   conteúdo. Tem relógio de segurança no JS e asserção no teste.
