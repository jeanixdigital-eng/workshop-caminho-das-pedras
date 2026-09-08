# Página de venda do Workshop — regras deste repositório

**Frente: Workshop (`@dieymisson_`).** Nunca a Clinix System: paleta, fonte e copy são desta frente.

- **A copy é da Lia** (`rascunho/copy.md`) e entra na página palavra por palavra. Mudou copy: muda no `copy.md` primeiro, depois no HTML. Regras que mandam: cofre `20 Estratégia/` (Tom de Voz, Restrições de Conteúdo, Regras do CFO). ⛔ Sem travessão no meio de frase, sem superlativo, sem urgência fabricada, sem promessa de resultado, sem preço de procedimento.
- **A estrutura é do Gael** (`rascunho/estrutura.md`). O formulário posta em `https://n8n-webhook.clinixsystem.com.br/webhook/wcp/form/lead` e recebe de volta o link de pagamento da pessoa. Campos e contrato estão no §2 da estrutura; não mude nome de campo sem mudar o porteiro (`jarvis-n8n-clinix/workshop/motores_wcp.py`).
- **Versão de trabalho:** `noindex`, `robots.txt` com `Disallow: /`, faixa amarela com a contagem de `<mark class="pendente">`. Publicar de verdade exige zero marcas, o parecer da Alba (08/09) resolvido e o domínio.
- **Prova antes de qualquer push:** `python3 testes/medir.py --simular` tem de dar 0 🔴. `--enviar` posta de verdade (só telefone da faixa de teste).
- `politica_versao` do formulário = linha de versão no topo de `privacidade.html`. Mudou a política, muda os dois.
- ⛔ Aqui não entra segredo, PII, dado de cliente. Nenhum número de paciente.
