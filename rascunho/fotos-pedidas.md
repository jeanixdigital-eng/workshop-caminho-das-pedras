---
tipo: pedido de material
frente: workshop
peça: página de venda do workshop (index.html)
criado: 2026-09-08
autor: Gael (mkt.site)
de quem depende: Dr. Dieymisson Mendes
---

# As fotos que faltam na página, e o que pedir ao Dr. Dieymisson

## O que é

A página de venda do workshop **nomeia uma pessoa real** e põe o número do CRO ao
lado do nome. Ela vende a autoridade dele: "eu sou dentista, tenho clínica, e
mostro a conta que a sua clínica não faz". Numa página assim, o rosto não é
enfeite, é a prova.

**Medido em 08/09/2026, com varredura do disco inteiro:** não existe **nenhuma**
foto do Dr. Dieymisson em `jarvis-marketing-clinix/`, `jarvis-cofre-workshop/`,
`carrosseis-virais/`, `jarvis-site-workshop/` nem em qualquer outro lugar do VPS.
O que existe de imagem é logo, slide de carrossel e frame gerado por IA da série
da Clinix, nada disso é ele.

## ⛔ A trava que não se negocia

**Rosto de banco de imagem, rosto genérico ou rosto gerado por IA apresentado
como o Dr. Dieymisson está proibido.** Não é preciosismo: é mentira sobre pessoa
identificável, com registro profissional impresso ao lado, numa peça pública que
existe justamente para dizer *"eu não prometo, eu mostro"*. Uma foto falsa
derruba a página inteira, e derruba a marca junto.

**O que a página faz enquanto a foto não chega** (já está no ar na versão de
trabalho): o lugar dela existe, com a proporção certa (4:5), uma placa
tipográfica com as iniciais **DM** e a marca amarela de pendência. Ninguém é
enganado, e o dia em que a foto chegar é só trocar a placa pela `<img>`.

Os **objetos** que ilustram a página hoje (cadeira, planilha, agenda, pasta de
orçamentos, sala vazia) foram **gerados por IA de propósito e são objetos, não
pessoas**. Nenhum deles é apresentado como fotografia da clínica dele.

---

## As 4 fotos, em ordem de importância

### 1. O retrato (esta é a que trava a página)

| | |
|---|---|
| **Onde entra** | Seção "Quem faz a conta com você", ao lado do texto. Substitui a placa `DM` |
| **Enquadramento** | **Vertical, 4:5.** Da cintura para cima, ou meio corpo. Ele ocupa a metade central do quadro |
| **Arquivo** | ≥ 1600 × 2000 px, JPG ou HEIC direto da câmera. Sem filtro, sem moldura, sem texto |
| **Onde** | Dentro da clínica dele, sentado à mesa com o computador. **O mesmo enquadramento do Reel "Dia 19 de outubro"** — quem vier do Reel precisa reconhecer o lugar na hora |
| **Luz** | Luz de janela, de lado. Nada de flash direto na cara |
| **Ele** | Olhando para a câmera, expressão neutra ou levemente séria. Jaleco ou scrub. ⛔ Sem sorriso de propaganda: a página não promete resultado, e o rosto tem de combinar |
| **⛔ Não pode aparecer** | Nenhuma tela com nome de paciente legível, nenhum paciente ao fundo, nenhum prontuário aberto, nenhuma foto de boca na parede (Regras do CFO + LGPD) |

### 2. A mesa onde a conta é feita

| | |
|---|---|
| **Onde entra** | Seção "A conta", no lugar da planilha 3D gerada, se ele preferir o real |
| **Enquadramento** | **Horizontal, 3:2.** De cima, a mesa dele com o extrato, a agenda e a calculadora |
| **⛔ Não pode aparecer** | Nenhum número de paciente, nenhum nome, nenhum CPF, nenhum valor de procedimento legível. Se tiver, é papel em branco na foto |

### 3. A cadeira dele, vazia

| | |
|---|---|
| **Onde entra** | Topo da página, no lugar da cadeira 3D gerada |
| **Enquadramento** | **Quadrado, 1:1.** Uma cadeira da clínica dele, vazia, sem ninguém no quadro |
| **Por que vale a pena trocar** | A cadeira 3D é bonita e é honesta (é uma ilustração, e o `alt` diz isso). A cadeira dele é a **dele** — e a página inteira vive de "este número é meu, desta clínica" |
| **⛔** | Ninguém sentado, nenhum profissional, nenhuma parte de paciente |

### 4. A clínica fechada

| | |
|---|---|
| **Onde entra** | Fundo da seção "A conta", no lugar da sala gerada |
| **Enquadramento** | **Horizontal, 3:2.** A sala de atendimento no fim do expediente, luz baixa, vazia |
| **Para quê** | É a primeira linha da conta: *"tudo que a clínica paga por mês mesmo de porta fechada"* |
| **⛔** | Ninguém no quadro. Nenhuma placa ou tela legível |

---

## Como mandar

Pelo WhatsApp mesmo, **como documento e não como imagem** (o WhatsApp comprime
foto enviada como imagem e o arquivo chega pequeno demais para o retrato). Ou
qualquer link de Drive.

Se der para tirar as quatro no mesmo dia, melhor: mesma luz, mesma roupa, mesma
clínica, e a página fica com uma cara só.

---

## Como foi testado

Ainda **não** foi: nenhuma das quatro existe. O que está provado é o
comportamento **sem** elas — `python3 testes/medir.py --simular` fecha em 0 🔴
com o slot do retrato no ar como placa tipográfica, e as capturas em
`testes/capturas/` mostram como a seção fica hoje.

## O que não repetir

1. **Não pedir "uma foto"** e esperar que venha o que serve. O pedido anterior
   ficava numa linha do `estrutura.md` (§6) e nunca virou caixinha rastreada no
   cofre — por isso continua aberto. Este arquivo diz enquadramento, proporção,
   tamanho, luz, roupa e o que **não** pode entrar no quadro.
2. **Não preencher o buraco com rosto que não é o dele.** Nem "só para ver o
   layout": provisório em página vira definitivo.
3. **Não aceitar foto com paciente, prontuário ou tela legível**, por mais bonita
   que seja. Volta para o Dr. Dieymisson pedindo outra.
