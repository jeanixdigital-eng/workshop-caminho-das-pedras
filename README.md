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
