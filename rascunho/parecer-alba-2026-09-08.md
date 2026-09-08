# Parecer da Alba (gate de conformidade) — página de venda do Workshop · 08/09/2026

**Peça:** `index.html` + `privacidade.html` + `assets/pagina.js` (versão de trabalho).
**Base:** cofre `20 Estratégia/` (Regras do CFO, Restrições de Conteúdo, Tom de Voz, Escada de Produtos) + dossiê CFO/LGPD do squad. **Não validado por advogado.**
**Enunciado dado a ela:** "prove que esta página viola alguma regra". Zero achados só valeria com o que foi verificado citado.

## Item a item

| # | Item | Veredito | O que foi medido |
|:-:|---|:-:|---|
| 1 | Preço de procedimento odontológico | ✅ | Todo `R$` é o ingresso (R$ 97) ou número da conta da clínica dele. `implante`/`manutenção`: zero ocorrências (a copy os deixou de fora de propósito) |
| 2 | Promessa ou insinuação de resultado | ✅ + 🟡 | A conta narra perdas da clínica **dele**, nunca ganho para o leitor; rodapé e FAQ recusam a promessa. Aritmética conferida. 🟡 A frase dos 35% é frase-âncora autorizada para o Reel; a página é uma quarta aparição, pública e permanente: pedir ao Dr. Dieymisson que estenda a decisão por escrito |
| 3 | Superlativo / comparativo | ✅ | Varredura: zero. "a conta mais simples" qualifica o método, não o profissional |
| 4 | Urgência / escassez | ✅ | Só a negação ("não tem contagem regressiva… nem últimas vagas") e "últimos 90 dias" (janela de medição) |
| 5 | Depoimento, paciente, cliente | ✅ | Zero. "Dental Center" é a clínica do apresentador (regra 6 das Restrições a faz fonte única de número); a autorização escrita que a regra 3 exige é o D4 |
| 6 | Identificação (nome + CRO) | 🟡 | Nome presente nos 6 slots; **número pendente nos 6** (sem ele a página não sobe). 🟡 "implantodontia e prótese": só especialidade inscrita no CRO pode ser anunciada; confirmar sim/não com o Dr. |
| 7 | Travessão no meio de frase | ✅ | U+2014, U+2013, `&mdash;`, `&ndash;` nos três arquivos: zero |
| 8 | Mentoria, Clinix, gravado como venda | 🟡 | Zero venda. FAQ afirma que existe oferta à parte com a gravação: contradiz a W13 (48 h para quem faltou) e depende do B3 (aberto desde 24/08). Marcado PENDENTE; antes de publicar, o Bruno fecha ou a frase sai. "Vendido por Clinix System": identificação do vendedor, decisão do Jean |
| 9 | LGPD | 🔴 → corrigido | 🔴 A caixa de aceite não nomeava a mensagem pós-workshop que a política §3/§4 dizia coberta por ela (finalidade específica). **Corrigido no mesmo turno** na página e na copy. ✅ Caixa `required` sem `checked`; link para a política; controlador, finalidades, fornecedores, transferência, prazo, direitos, canal; zero artigo de lei; `politica_versao` = versão da política; pixel não carrega sem id; servidor recusa sem aceite e grava versão + hora. 🟡 Quando o pixel existir: aceite antes de carregar (posição do gate) |
| 10 | Fidelidade à copy da Lia | ✅ | Diff do texto visível × `copy.md`: só "Pular para o conteúdo", o rótulo do honeypot, "Por hora de cadeira" (derivado) e a faixa de trabalho. Mensagens do JS batem uma a uma |
| 11 | Outros | 🟡 | 17 marcas `pendente` (9 + 8) e a faixa: publicar = zero marcas. "O link da sala chega 15 minutos antes" depende da W10. Conferir que "SAIR" é a palavra do opt-out. Reconferir o capítulo de publicidade do CFO antes de 19/10 (grupo de trabalho em curso). Endereço do controlador lê-se incompleto |

## Veredito
**Versão de trabalho:** REPROVADA por um achado (item 9), **corrigido no mesmo turno**. Com a correção, o que resta é 🟡 de gente, não de texto.

**Antes de publicar de verdade, por quem decide:**
1. **Dr. Dieymisson:** D4 por escrito no cofre (expor os números de agosto); estender a decisão dos 35% à página; confirmar as especialidades inscritas; o número do CRO nos seis slots; horário e duração; foto.
2. **Bruno:** fechar B3 (bump) e decidir a W13; ajustar ou remover a frase da FAQ sobre a gravação.
3. **Jean:** quem vende e é controlador; aceite antes do pixel; prazo de 90 dias; confirmar que a W10 entrega o link 15 min antes; endereço do controlador; domínio próprio; remover faixa e marcas.

## O que a Alba não verificou (declarado por ela)
Registro de recusa "só com hora e motivo" (mediu só que o 400 leva o código e que o contador por IP existe); se o aceite chega ao GHL como a tabela §5 diz (fica no evento do banco `wcp`); se "SAIR" é a palavra do opt-out; exclusão aos 90 dias; quem lê `contact@clinixsystem.com.br` em 15 dias; a hospedagem final; o CSS e o `og.png`.
