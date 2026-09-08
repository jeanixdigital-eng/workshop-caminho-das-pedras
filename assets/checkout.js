/* Página de pagamento do Workshop · assets/checkout.js · só o checkout.html usa.
   Contrato do servidor (medido em 08/09/2026):
     GET  /webhook/wcp/checkout/sessao?c=<token>   → 200 {ok,valor,primeiro_nome,email,public_key,max_parcelas,teste,expira_em}
                                                     404 SESSAO_EXPIRADA_OU_INEXISTENTE · 503 MP_DESLIGADO
     POST /webhook/wcp/pagamento/criar             → 200 {ok,payment_id,status,status_detail,metodo,pix?}
                                                     400 <codigo> · 429 MUITAS_TENTATIVAS · 502 PAGAMENTO_INDISPONIVEL · 503 MP_DESLIGADO
   🔑 O POST vai em JSON. O preflight OPTIONS do endereço foi medido em 08/09 e
      responde 204 com `access-control-allow-headers: content-type`, então o
      `Content-Type: application/json` passa. ⛔ Nenhum cabeçalho nosso: a porta é
      pública e a credencial é o token da sessão, que vem da URL.
   ⛔ Nada aqui escreve CSS mirando classe do Brick: os nomes são gerados no build
      do Mercado Pago. O visual dele sai de `theme` + `customVariables`, e os
      valores dessas variáveis são lidos dos tokens do Nocturne em tempo de
      execução, para o Brick nunca sair do sistema quando alguém retunar o tema.
   ⛔ Sem JavaScript esta página não paga. É o contrário da página de venda, e é
      inevitável: quem embaralha o cartão no navegador é o código do Mercado Pago. */
(function () {
  'use strict';

  /* O identificador do aparelho, nas tres vias que existem, em ordem de confianca.
     🔑 Medido em 08/09: a doc do Mercado Pago diz que o SDK JS ja entrega isso em
     `MP_DEVICE_SESSION_ID` e NAO entrega. Quem entrega e o security.js, que a
     pagina carrega logo depois do SDK. A terceira via (a chave global `armor.`)
     fica como rede: se o script mudar de nome de variavel, o valor ainda esta la,
     guardado no NOME da global.
     ⛔ Sem este valor o antifraude recusa cartao legitimo por "risco alto". */
  function idDoAparelho() {
    try {
      if (typeof window.idDoAparelho === 'string' && window.idDoAparelho) return window.idDoAparelho;
      if (typeof window.MP_DEVICE_SESSION_ID === 'string' && window.MP_DEVICE_SESSION_ID) return window.MP_DEVICE_SESSION_ID;
      var k = Object.keys(window).find(function (n) { return n.indexOf('armor.') === 0; });
      if (k) return k;
    } catch (e) {}
    return '';
  }


  var BASE = 'https://n8n-webhook.clinixsystem.com.br';
  var URL_SESSAO = BASE + '/webhook/wcp/checkout/sessao';
  var URL_PAGAR = BASE + '/webhook/wcp/pagamento/criar';
  var URL_ESTADO = BASE + '/webhook/wcp/pagamento/estado';

  var el = function (id) { return document.getElementById(id); };
  var estado = el('estado'), recusa = el('recusa'), recusaTexto = el('recusa-texto');
  var erroPag = el('erro-pagamento'), caixaCpf = el('cpf-bloco'), campoCpf = el('cpf');
  var erroCpf = el('erro-cpf'), botaoCpf = el('cpf-segue');
  var caixaPix = el('pix'), imgPix = el('pix-qr'), codPix = el('pix-codigo');
  var prazoPix = el('pix-prazo'), copiado = el('pix-copiado');
  var linhaVigia = el('pix-vigia'), caixaPago = el('pago'), caixaAcoes = el('pix-acoes');

  var sessao = null, token = null, controlador = null, emailPix = '', pronto = false;

  /* ---------- Faixa "versão de trabalho": conta as pendências que estão no DOM ---------- */
  var n = el('n-pendencias');
  if (n) n.textContent = String(document.querySelectorAll('.pendente').length);

  /* ---------- Textos. Frase curta, "você", sem culpar quem está pagando ---------- */
  var MSG = {
    SEM_TOKEN: 'Este endereço veio sem o código do seu pagamento. Volte à página do workshop e deixe o seu contato de novo: o link do pagamento chega em seguida.',
    SESSAO_EXPIRADA_OU_INEXISTENTE: 'Este link de pagamento não vale mais. Ele tem prazo, e o seu venceu. Deixe o seu contato de novo e eu te mando um link novo na hora.',
    SESSAO_INVALIDA: 'Este link de pagamento não vale mais. Deixe o seu contato de novo e eu te mando um link novo na hora.',
    MP_DESLIGADO: 'O pagamento está fora do ar agora, e o problema é do nosso lado, não seu. Tente de novo em alguns minutos.',
    SEM_REDE: 'Não consegui falar com o servidor. Confira a sua internet e recarregue a página.',
    SEM_SDK: 'O código do Mercado Pago não carregou nesta página. Recarregue. Se continuar, tente por outro navegador ou pelo celular.',
    SEM_CHAVE: 'O pagamento não pôde ser aberto agora, e o problema é do nosso lado, não seu. Me chama no direct do @dieymisson_ que eu resolvo.',
    BRICK_FALHOU: 'O formulário de pagamento não abriu. Recarregue a página. Se continuar, me chama no direct do @dieymisson_.',
    MUITAS_TENTATIVAS: 'Foram muitas tentativas seguidas daqui. Espere uma hora e tente de novo.',
    PAGAMENTO_INDISPONIVEL: 'A cobrança não foi criada, e o problema é do nosso lado, não seu. Tente de novo em alguns minutos.',
    IDEMPOTENCIA_INVALIDA: 'O envio não passou. Recarregue a página e tente de novo.',
    DADO_DE_CARTAO_RECUSADO: 'O envio não passou. Recarregue a página e tente de novo.',
    TOKEN_AUSENTE: 'Os dados do cartão não foram lidos. Preencha o cartão de novo e envie.',
    METODO_AUSENTE: 'Escolha a forma de pagamento antes de enviar.',
    EMAIL_INVALIDO: 'O e-mail não passou. Confira se está completo, com o @ e o ponto.',
    CPF_INVALIDO: 'O CPF não passou. Ele tem 11 dígitos. Confira e envie de novo.',
    GENERICO: 'O pagamento não passou agora. Tente de novo em alguns minutos. Se continuar, me chama no direct do @dieymisson_.',
    SEM_EMAIL: 'Preciso do seu e-mail para gerar o Pix. Preencha o e-mail no formulário de pagamento e tente de novo.'
  };

  /* Motivo da recusa do cartão, em português. O texto diz o que fazer agora e
     não trata a pessoa como culpada: quem recusa é o banco dela. */
  var RECUSA_CARTAO = {
    cc_rejected_insufficient_amount: 'O cartão não tinha limite para este valor. Você pode usar outro cartão ou pagar no Pix.',
    cc_rejected_bad_filled_security_code: 'O código de segurança não bateu. Confira os três dígitos do verso do cartão e envie de novo.',
    cc_rejected_bad_filled_date: 'A validade não bateu. Confira o mês e o ano impressos no cartão e envie de novo.',
    cc_rejected_bad_filled_card_number: 'O número do cartão não bateu. Confira os dígitos e envie de novo.',
    cc_rejected_bad_filled_other: 'Algum dado do cartão não bateu. Confira número, validade, código de segurança e CPF, e envie de novo.',
    cc_rejected_call_for_authorize: 'O seu banco precisa autorizar esta compra. Ligue para o número do verso do cartão, autorize o valor, e envie de novo aqui.',
    cc_rejected_high_risk: 'O banco não autorizou esta compra. Você pode usar outro cartão ou pagar no Pix.',
    cc_rejected_card_disabled: 'Este cartão está desativado para compra pela internet. Ligue para o seu banco ou use outro cartão.',
    cc_rejected_duplicated_payment: 'Este pagamento já foi feito. Confira o seu WhatsApp antes de pagar de novo.',
    cc_rejected_max_attempts: 'Foram muitas tentativas com este cartão. Use outro cartão ou pague no Pix.',
    cc_rejected_invalid_installments: 'Este cartão não aceita esse número de parcelas. Escolha outro parcelamento e envie de novo.',
    cc_rejected_other_reason: 'O banco não autorizou esta compra e não disse o motivo. Você pode usar outro cartão ou pagar no Pix.'
  };

  /* ---------- Utilidades ---------- */

  function texto(elemento, t) { if (elemento) { elemento.textContent = t; } }

  function moeda(v) {
    try { return v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }); }
    catch (e) { return 'R$ ' + v.toFixed(2).replace('.', ','); }
  }

  function quandoVence(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    try {
      return d.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
    } catch (e) { return ''; }
  }

  /* UUID v4 novo a cada envio. `crypto.randomUUID` só existe em contexto seguro;
     o resto do caminho usa `getRandomValues`, que existe desde sempre. */
  function uuid() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') return window.crypto.randomUUID();
    var b = new Uint8Array(16);
    (window.crypto || window.msCrypto).getRandomValues(b);
    b[6] = (b[6] & 0x0f) | 0x40; b[8] = (b[8] & 0x3f) | 0x80;
    var h = [];
    for (var i = 0; i < 16; i++) h.push((b[i] + 0x100).toString(16).slice(1));
    return h.slice(0, 4).join('') + '-' + h.slice(4, 6).join('') + '-' + h.slice(6, 8).join('') +
           '-' + h.slice(8, 10).join('') + '-' + h.slice(10, 16).join('');
  }

  /* "@dieymisson_" vira link, como na página de venda. */
  function comLink(t) {
    var alvo = '@dieymisson_', i = t.indexOf(alvo), frag = document.createDocumentFragment();
    if (i < 0) { frag.appendChild(document.createTextNode(t)); return frag; }
    frag.appendChild(document.createTextNode(t.slice(0, i)));
    var a = document.createElement('a');
    a.href = 'https://www.instagram.com/dieymisson_/'; a.target = '_blank'; a.rel = 'noopener'; a.textContent = alvo;
    frag.appendChild(a);
    frag.appendChild(document.createTextNode(t.slice(i + alvo.length)));
    return frag;
  }

  /* Recusa: a sessão não serve, ou o formulário não abriu. O Brick NÃO é
     montado, e a pessoa ganha um caminho em vez de uma tela morta.
     O caminho muda com o motivo: sessão vencida se resolve deixando o contato
     de novo; formulário que não abriu se resolve recarregando. */
  function mostraRecusa(codigo) {
    if (estado) estado.hidden = true;
    if (recusaTexto) { recusaTexto.textContent = ''; recusaTexto.appendChild(comLink(MSG[codigo] || MSG.GENERICO)); }
    /* Sessão recusada é pedido que não existe: a linha do total sai da tela em
       vez de ficar "carregando" para sempre. O que sobra no resumo continua
       verdadeiro (o que é o workshop e quando é). */
    var total = el('total');
    if (total) total.hidden = true;
    var botao = el('recusa-volta');
    if (botao && (codigo === 'BRICK_FALHOU' || codigo === 'SEM_SDK' || codigo === 'SEM_REDE')) {
      botao.href = location.href;
      botao.textContent = 'Recarregar a página';
    }
    if (recusa) recusa.hidden = false;
  }

  /* Erro de tentativa: a sessão continua boa, o Brick continua na tela.
     `neutro` é o recado que não é erro (pagamento em análise, falta o CPF): ele
     não vai de vermelho, senão o vermelho deixa de significar erro. */
  function mostraErro(codigo, textoDireto, neutro) {
    if (!erroPag) return;
    erroPag.textContent = '';
    erroPag.className = neutro ? 'erro-pagamento aviso' : 'erro-pagamento';
    erroPag.appendChild(comLink(textoDireto || MSG[codigo] || MSG.GENERICO));
    erroPag.setAttribute('tabindex', '-1');
    try { erroPag.focus({ preventScroll: false }); } catch (e) { erroPag.focus(); }
  }
  function limpaErro() { if (erroPag) { erroPag.textContent = ''; erroPag.className = 'erro-pagamento'; } }

  /* ---------- 1. O token da URL ---------- */

  token = new URLSearchParams(location.search).get('c') || '';
  /* Mesma régua do servidor (`validaEntrada`): letras e números, 24 a 48. O
     token de hoje são 48 dígitos hexadecimais sorteados pelo banco. */
  if (!/^[A-Za-z0-9]{24,48}$/.test(token)) { mostraRecusa('SEM_TOKEN'); return; }

  /* ---------- 2. A sessão ---------- */

  function pedeSessao() {
    var ctrl = new AbortController();
    var t = setTimeout(function () { ctrl.abort(); }, 20000);
    fetch(URL_SESSAO + '?c=' + encodeURIComponent(token), { method: 'GET', signal: ctrl.signal })
      .then(function (r) {
        return r.json().catch(function () { return null; }).then(function (j) {
          if (r.ok && j && j.ok === true) return abreSessao(j);
          if (r.status === 503 || (j && j.codigo === 'MP_DESLIGADO')) return mostraRecusa('MP_DESLIGADO');
          if (r.status === 404 || (j && j.codigo)) return mostraRecusa((j && j.codigo) || 'SESSAO_EXPIRADA_OU_INEXISTENTE');
          mostraRecusa('SEM_REDE');
        });
      })
      .catch(function () { mostraRecusa('SEM_REDE'); })
      .then(function () { clearTimeout(t); });
  }

  function abreSessao(j) {
    sessao = j;
    var valor = Number(j.valor);
    if (!isFinite(valor) || valor <= 0) return mostraRecusa('SEM_CHAVE');

    /* O valor da tela é SEMPRE o que veio do servidor. Não existe número de
       preço escrito no HTML desta página. */
    var caixaValor = el('valor');
    if (caixaValor) caixaValor.textContent = moeda(valor);

    if (j.teste === true) { var f = el('faixa-teste'); if (f) f.hidden = false; }

    var primeiro = String(j.primeiro_nome || '').trim().split(/\s+/)[0];
    var saudacao = el('saudacao');
    if (primeiro && saudacao) {
      saudacao.textContent = 'Recebi o seu contato, ' + primeiro + '. Assim que o pagamento cair, o acesso chega no seu WhatsApp.';
    }

    montaBrick(valor);
  }

  /* ---------- 3. O Brick ---------- */

  /* O tema do Brick sai dos tokens do Nocturne, lidos do documento. Se um token
     mudar no design system, o Brick muda junto e ninguém precisa lembrar daqui. */
  function tok(nome, reserva) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(nome).trim();
    return v || reserva;
  }

  function montaBrick(valor) {
    if (typeof window.MercadoPago !== 'function') return mostraRecusa('SEM_SDK');
    if (!sessao.public_key) return mostraRecusa('SEM_CHAVE');

    var mp, bricks;
    try { mp = new window.MercadoPago(sessao.public_key); bricks = mp.bricks(); }
    catch (e) { return mostraRecusa('SEM_CHAVE'); }

    var parcelas = Math.max(1, Number(sessao.max_parcelas || 1));
    var config = {
      initialization: {
        amount: valor,
        payer: { email: sessao.email || undefined }
      },
      customization: {
        /* ⛔ Para EXCLUIR um meio, a chave sai do objeto. Lista vazia não exclui,
           e por isso `ticket`, `mercadoPago` e `atm` simplesmente não estão aqui. */
        paymentMethods: {
          creditCard: 'all',
          bankTransfer: 'all',
          maxInstallments: parcelas
        },
        visual: {
          style: {
            theme: 'dark',
            customVariables: {
              formBackgroundColor: tok('--color-surface', '#232532'),
              inputBackgroundColor: tok('--color-bg', '#161826'),
              textPrimaryColor: tok('--color-text', '#e9e9ed'),
              textSecondaryColor: tok('--color-neutral-400', '#b2b6ca'),
              baseColor: tok('--color-accent', '#9184d9'),
              buttonTextColor: tok('--color-bg', '#161826'),
              borderRadiusMedium: tok('--radius-md', '8px'),
              fontSizeSmall: '14px'
            }
          }
        }
      },
      callbacks: {
        onReady: function () { pronto = true; if (estado) estado.hidden = true; },
        onSubmit: aoEnviar,
        onError: function (erro) {
          /* O Brick chama isto tanto no erro de montagem quanto no erro de
             preenchimento dele. Se ele nunca ficou pronto, é montagem. */
          if (!pronto) { mostraRecusa('BRICK_FALHOU'); return; }
          if (erro && erro.message) mostraErro(null, 'Confira os dados do pagamento e envie de novo.');
        }
      }
    };

    /* 🔑 Vigia de montagem. Medido em 08/09 com uma chave pública que o Mercado
       Pago não reconhece: `create` NÃO resolve nem rejeita, e a página ficaria
       para sempre em "Carregando o pagamento". Silêncio é falha, e aqui ele tem
       prazo. */
    setTimeout(function () { if (!pronto) mostraRecusa('BRICK_FALHOU'); }, 20000);

    bricks.create('payment', 'brick', config)
      .then(function (c) { controlador = c || window.paymentBrickController || null; })
      .catch(function () { mostraRecusa('BRICK_FALHOU'); });
  }

  function desmonta() {
    var c = controlador || window.paymentBrickController;
    if (c && typeof c.unmount === 'function') { try { c.unmount(); } catch (e) {} }
    controlador = null;
  }
  window.addEventListener('pagehide', desmonta);

  /* ---------- 4. O envio ---------- */

  /* O Brick entrega `formData`. O CPF do cartão vem em `payer.identification`.
     ⚠️ No Pix a documentação se contradiz (o texto pede documento, o tipo do
     formulário de Pix só declara e-mail) e não foi possível medir com o Brick de
     verdade em 08/09 (a chave pública guardada é recusada pelo Mercado Pago com
     "public key not found"). Então o desenho não aposta: se o CPF não vier, a
     nossa página pede, com campo próprio, e o Pix segue pelo nosso botão, que
     não depende de nada do Brick. */
  function aoEnviar(dados) {
    dados = dados || {};
    var forma = dados.selectedPaymentMethod || '';
    var f = dados.formData || {};
    var pagador = f.payer || {};
    var cpfDoBrick = String((pagador.identification && pagador.identification.number) || '').replace(/\D/g, '');
    var ehPix = forma === 'bank_transfer' || f.payment_method_id === 'pix';
    limpaErro();

    if (ehPix) {
      emailPix = String(pagador.email || sessao.email || '');
      var cpf = cpfDoBrick || digitos(campoCpf ? campoCpf.value : '');
      if (cpf.length !== 11) {
        pedeCpf();
        return Promise.reject();
      }
      pedidoPix = { email: emailPix, cpf: cpf };
      return seguiu(envia(montaPedido('bank_transfer', { payment_method_id: 'pix', email: emailPix, cpf: cpf })));
    }

    return seguiu(envia(montaPedido(forma || 'credit_card', {
      token: String(f.token || ''),
      payment_method_id: String(f.payment_method_id || ''),
      installments: Number(f.installments || 1),
      issuer_id: String(f.issuer_id || ''),
      email: String(pagador.email || sessao.email || ''),
      cpf: cpfDoBrick || digitos(campoCpf ? campoCpf.value : '')
    })));
  }

  /* O Brick lê a promessa do `onSubmit`: resolvida é "seguiu", rejeitada é
     "continua na tela para tentar de novo". Cobrança recusada pelo banco é o
     segundo caso, e é o que devolve o formulário preenchido para a pessoa. */
  function seguiu(promessa) {
    return promessa.then(function (ok) { if (!ok) return Promise.reject(); });
  }

  function montaPedido(tipo, extra) {
    var p = {
      idempotencia: uuid(),
      token_sessao: token,
      tipo: tipo,
      token: '',
      payment_method_id: '',
      installments: 1,
      issuer_id: '',
      email: '',
      cpf: '',
      device_id: idDoAparelho()
    };
    for (var k in extra) { if (Object.prototype.hasOwnProperty.call(extra, k)) p[k] = extra[k]; }
    return p;
  }

  function envia(pedido) {
    var ctrl = new AbortController();
    var t = setTimeout(function () { ctrl.abort(); }, 30000);
    return fetch(URL_PAGAR, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(pedido),
      signal: ctrl.signal
    })
      .then(function (r) {
        return r.json().catch(function () { return null; }).then(function (j) {
          if (r.ok && j && j.ok === true) return resultado(j);
          var codigo = (j && j.codigo) ||
            (r.status === 429 ? 'MUITAS_TENTATIVAS' : r.status === 503 ? 'MP_DESLIGADO' :
             r.status === 502 ? 'PAGAMENTO_INDISPONIVEL' : 'GENERICO');
          if (codigo === 'SESSAO_EXPIRADA_OU_INEXISTENTE' || codigo === 'SESSAO_INVALIDA') {
            desmonta();
            mostraRecusa(codigo);
            return true;   /* a tela mudou de estado: o Brick não volta */
          }
          if (codigo === 'CPF_INVALIDO') pedeCpf(true);
          mostraErro(codigo);
          return false;
        });
      })
      .catch(function () { mostraErro('SEM_REDE'); return false; })
      .then(function (ok) { clearTimeout(t); return ok; });
  }

  /* ---------- 5. O que fazer com o resultado ---------- */

  /* Devolve `true` quando a tela seguiu adiante (aprovado, Pix na tela, análise)
     e `false` quando a pessoa precisa tentar de novo no mesmo formulário. */
  function resultado(j) {
    var estadoPag = String(j.status || '');
    if (estadoPag === 'approved') {
      desmonta();
      location.assign('obrigado.html?p=' + encodeURIComponent(String(j.payment_id || '')));
      return true;
    }
    if (j.pix && j.pix.qr_code) { mostraPix(j.pix, j.payment_id); return true; }
    if (estadoPag === 'rejected') {
      mostraErro(null, RECUSA_CARTAO[j.status_detail] ||
        'O pagamento não foi autorizado. Você pode usar outro cartão ou pagar no Pix.');
      return false;
    }
    if (estadoPag === 'in_process' || estadoPag === 'pending') {
      desmonta();
      mostraErro(null, 'O seu pagamento está em análise pelo Mercado Pago. Assim que ele confirmar, o acesso chega no seu WhatsApp. Você não precisa pagar de novo.', true);
      return true;
    }
    mostraErro('GENERICO');
    return false;
  }

  /* ---------- 6. Pix na nossa página ---------- */

  function mostraPix(pix, idPagamento) {
    desmonta();
    limpaErro();
    if (caixaCpf) caixaCpf.hidden = true;
    if (estado) estado.hidden = true;
    /* Um Pix novo apaga o que sobrou do anterior: confirmação, caminhos de
       recomeço e a linha do vigia. */
    if (caixaPago) caixaPago.hidden = true;
    if (caixaAcoes) caixaAcoes.hidden = true;
    texto(copiado, '');
    if (imgPix && pix.qr_code_base64) { imgPix.src = 'data:image/png;base64,' + pix.qr_code_base64; imgPix.hidden = false; }
    else if (imgPix) imgPix.hidden = true;
    if (codPix) codPix.value = String(pix.qr_code || '');
    var quando = pix.expira_em ? quandoVence(pix.expira_em) : '';
    texto(prazoPix, quando ? 'O código vale até ' + quando + '.' : '');
    if (caixaPix) caixaPix.hidden = false;
    if (caixaPix) { caixaPix.setAttribute('tabindex', '-1'); try { caixaPix.focus(); } catch (e) {} }
    comecaVigia(idPagamento, pix.expira_em);
  }

  if (el('pix-copiar')) {
    el('pix-copiar').addEventListener('click', function () {
      var valor = codPix ? codPix.value : '';
      if (!valor) return;
      var pronto = function () { texto(copiado, 'Código copiado. Cole no aplicativo do seu banco.'); };
      var falhou = function () { texto(copiado, 'Não consegui copiar daqui. Selecione o código acima e copie.'); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(valor).then(pronto).catch(function () {
          codPix.select();
          try { document.execCommand('copy') ? pronto() : falhou(); } catch (e) { falhou(); }
        });
      } else {
        codPix.select();
        try { document.execCommand('copy') ? pronto() : falhou(); } catch (e) { falhou(); }
      }
    });
  }

  /* ---------- 7. O vigia do Pix: quem conta que o pagamento caiu ---------- */

  /* Porta pública, só de leitura:
       GET /webhook/wcp/pagamento/estado?c=<token da sessão>&p=<payment_id>
         200 {ok:true, pago:<bool>, status, status_detail, encerrado:<bool>}
         404 {ok:false, codigo:'PAGAMENTO_NAO_ENCONTRADO'}
     ⛔ Ela devolve SÓ estado: nada de valor, nome ou e-mail. A credencial é o
        token da sessão, que já está na URL desta página, e nenhum cabeçalho
        nosso vai junto.
     🔑 Cada pergunta daqui que o banco ainda não respondeu vira uma chamada ao
        Mercado Pago. Por isso o ritmo cresce, o laço tem fim e a aba escondida
        não pergunta nada. */

  var VIGIA_TETO = 2 * 60 * 60 * 1000;   /* teto absoluto do laço: 2 horas */
  var VIGIA_PADRAO = 30 * 60 * 1000;     /* prazo suposto quando o servidor não disse qual é */

  var vigia = { id: '', inicio: 0, venceEm: 0, timer: null, ativo: false, consultando: false };
  var pedidoPix = null;   /* e-mail e CPF do último Pix, para gerar outro sem pedir de novo */

  function agora() { return Date.now(); }

  /* Ritmo educado. O primeiro meio minuto é quando a pessoa está digitando a
     senha no aplicativo do banco, e é ali que responder rápido vale alguma
     coisa. Passado isso, a espera é do banco, não dela: perguntar de três em
     três segundos só gasta chamada nossa e do Mercado Pago. */
  function ritmo(decorrido) {
    if (decorrido < 30000) return 3000;
    if (decorrido < 120000) return 5000;
    return 10000;
  }

  var FIM_DO_PIX = {
    rejected: 'O banco não autorizou este Pix, e nada foi cobrado de você. Você pode gerar outro código agora ou pagar no cartão.',
    cancelled: 'Este Pix foi cancelado antes de ser pago, e nada foi cobrado de você. Você pode gerar outro código agora ou pagar no cartão.',
    refunded: 'Este pagamento foi devolvido. Se não foi você que pediu a devolução, me chama no direct do @dieymisson_.'
  };

  function vigiaTexto(t, esperando) {
    if (!linhaVigia) return;
    linhaVigia.className = esperando ? 'pix-vigia pix-vigia--esperando' : 'pix-vigia';
    linhaVigia.textContent = '';
    if (t) linhaVigia.appendChild(comLink(t));
  }

  function paraVigia() {
    vigia.ativo = false;
    if (vigia.timer) { clearTimeout(vigia.timer); vigia.timer = null; }
  }

  function agendaVigia() {
    if (vigia.timer) { clearTimeout(vigia.timer); vigia.timer = null; }
    if (!vigia.ativo || document.hidden) return;
    vigia.timer = setTimeout(bateVigia, ritmo(agora() - vigia.inicio));
  }

  function bateVigia() {
    if (vigia.timer) { clearTimeout(vigia.timer); vigia.timer = null; }
    if (!vigia.ativo || document.hidden) return;
    if (agora() >= vigia.venceEm) { paraVigia(); pixVenceu(); return; }
    if (vigia.consultando) { agendaVigia(); return; }
    vigia.consultando = true;
    var ctrl = new AbortController();
    var t = setTimeout(function () { ctrl.abort(); }, 15000);
    fetch(URL_ESTADO + '?c=' + encodeURIComponent(token) + '&p=' + encodeURIComponent(vigia.id),
          { method: 'GET', signal: ctrl.signal })
      .then(function (r) {
        return r.json().catch(function () { return null; }).then(function (j) {
          if (r.ok && j && j.ok === true) leEstado(j);
          /* ⛔ Resposta que não é 200 NÃO vira aviso na tela. Consulta é
             conferência, não é o pagamento: o dinheiro pode ter caído mesmo
             assim, e assustar quem acabou de pagar é pior do que ficar quieto.
             Tenta de novo no próximo ciclo, até o prazo do Pix acabar. */
        });
      })
      .catch(function () { /* rede caiu no meio: mesmo silêncio, mesma razão. */ })
      .then(function () { clearTimeout(t); vigia.consultando = false; agendaVigia(); });
  }

  function comecaVigia(id, expiraEm) {
    paraVigia();
    vigia.id = String(id || '');
    /* ⛔ Sem payment_id não há o que perguntar. Nada de laço no vazio. */
    if (!vigia.id) { vigiaTexto(''); return; }
    vigia.inicio = agora();
    var fim = expiraEm ? new Date(expiraEm).getTime() : 0;
    if (!isFinite(fim) || fim <= 0) fim = agora() + VIGIA_PADRAO;
    vigia.venceEm = Math.min(fim, agora() + VIGIA_TETO);
    if (agora() >= vigia.venceEm) { pixVenceu(); return; }
    vigia.ativo = true;
    vigiaTexto('Estou de olho aqui. Assim que o seu Pix cair, esta tela avisa.', true);
    agendaVigia();
  }

  function leEstado(j) {
    if (j.pago === true) { paraVigia(); pixCaiu(); return; }
    var s = String(j.status || '');
    if (s === 'rejected' || s === 'cancelled' || j.encerrado === true) { paraVigia(); pixNaoVale(s); }
  }

  function pixCaiu() {
    limpaErro();
    if (caixaPix) caixaPix.hidden = true;
    if (caixaAcoes) caixaAcoes.hidden = true;
    vigiaTexto('Pagamento aprovado. O acesso chega no seu WhatsApp.');
    if (caixaPago) { caixaPago.hidden = false; try { caixaPago.focus(); } catch (e) {} }
    marcaCompraNoPixel(vigia.id);
    /* Dois segundos para a pessoa ler a confirmação antes de a tela trocar. */
    setTimeout(function () {
      location.assign('obrigado.html?p=' + encodeURIComponent(vigia.id));
    }, 2000);
  }

  /* O pixel da Meta, se ele existir nesta página. `eventID` aqui é o mesmo
     número que o servidor manda como `event_id`: é por ele que a Meta junta os
     dois avisos e não conta a mesma venda duas vezes. */
  function marcaCompraNoPixel(id) {
    try {
      if (typeof window.fbq !== 'function') return;
      var v = sessao ? Number(sessao.valor) : NaN;
      var dados = { currency: 'BRL' };
      if (isFinite(v) && v > 0) dados.value = v;
      window.fbq('track', 'Purchase', dados, { eventID: String(id) });
    } catch (e) {}
  }

  /* O código morto sai da tela: ninguém deve pagar um Pix que não vale mais.
     ⛔ O texto de reserva não afirma que nada foi cobrado: num estado final que
        eu não conheço, quem sabe o que aconteceu com o dinheiro é o Mercado
        Pago, não esta tela. */
  function pixNaoVale(s) {
    if (caixaPix) caixaPix.hidden = true;
    vigiaTexto(FIM_DO_PIX[s] ||
      'O Mercado Pago encerrou este pagamento. Se você já pagou, a confirmação chega no seu WhatsApp. Se não chegar nada, me chama no direct do @dieymisson_.');
    mostraCaminhos();
  }

  function pixVenceu() {
    if (caixaPix) caixaPix.hidden = true;
    vigiaTexto('O prazo deste código venceu. Se você já pagou, fique tranquilo: a confirmação chega no seu WhatsApp. Se ainda não pagou, gere outro código agora.');
    mostraCaminhos();
  }

  function mostraCaminhos() {
    if (!caixaAcoes) return;
    caixaAcoes.hidden = false;
    var b = el('pix-refazer');
    if (b) { try { b.focus(); } catch (e) {} }
  }

  /* A aba escondida é a pessoa dentro do aplicativo do banco. Perguntar para uma
     tela que ninguém está vendo é gastar chamada à toa, e a volta para a aba é o
     instante exato em que a resposta importa: por isso a volta pergunta na hora,
     sem esperar o próximo ciclo. */
  document.addEventListener('visibilitychange', function () {
    if (!vigia.ativo) return;
    if (document.hidden) { if (vigia.timer) { clearTimeout(vigia.timer); vigia.timer = null; } return; }
    bateVigia();
  });
  window.addEventListener('pagehide', paraVigia);

  if (el('pix-refazer')) {
    el('pix-refazer').addEventListener('click', function () {
      var b = this;
      /* Sem o pedido guardado não dá para refazer daqui sem inventar dado:
         recarregar devolve a pessoa ao formulário, com a sessão da URL. */
      if (!pedidoPix) { location.reload(); return; }
      paraVigia();
      if (caixaAcoes) caixaAcoes.hidden = true;
      vigiaTexto('Gerando outro código do Pix.', true);
      b.disabled = true; b.setAttribute('aria-busy', 'true');
      envia(montaPedido('bank_transfer', { payment_method_id: 'pix', email: pedidoPix.email, cpf: pedidoPix.cpf }))
        .then(function (ok) {
          b.disabled = false; b.removeAttribute('aria-busy');
          if (!ok) { vigiaTexto(''); mostraCaminhos(); }
        });
    });
  }

  /* Pagar no cartão é voltar ao formulário do Mercado Pago. Recarregar é o
     caminho honesto: a sessão da URL continua valendo e o Brick monta de novo,
     com cartão e Pix. */
  if (el('pix-cartao')) {
    el('pix-cartao').addEventListener('click', function () { paraVigia(); location.reload(); });
  }

  /* ---------- 8. O CPF que o Brick não entrega ---------- */

  function digitos(v) { return String(v || '').replace(/\D/g, ''); }

  function pedeCpf(jaTentou) {
    if (!caixaCpf) return;
    caixaCpf.hidden = false;
    if (!jaTentou) {
      mostraErro(null, 'Falta um dado para o Pix: o Mercado Pago pede o CPF de quem paga. Preencha abaixo e siga.', true);
    }
    if (campoCpf) { try { campoCpf.focus(); } catch (e) {} }
  }

  if (campoCpf) {
    campoCpf.addEventListener('input', function () {
      var d = digitos(campoCpf.value).slice(0, 11);
      campoCpf.value = d.length > 9 ? d.replace(/^(\d{3})(\d{3})(\d{3})(\d{0,2}).*/, '$1.$2.$3-$4')
                     : d.length > 6 ? d.replace(/^(\d{3})(\d{3})(\d{0,3})/, '$1.$2.$3')
                     : d.length > 3 ? d.replace(/^(\d{3})(\d{0,3})/, '$1.$2') : d;
      if (campoCpf.getAttribute('aria-invalid')) {
        campoCpf.removeAttribute('aria-invalid');
        texto(erroCpf, '');
      }
    });
  }

  if (botaoCpf) {
    botaoCpf.addEventListener('click', function () {
      var cpf = digitos(campoCpf ? campoCpf.value : '');
      if (cpf.length !== 11) {
        campoCpf.setAttribute('aria-invalid', 'true');
        texto(erroCpf, 'O CPF tem 11 dígitos. Confira e digite de novo.');
        campoCpf.focus();
        return;
      }
      var email = emailPix || (sessao && sessao.email) || '';
      if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(email)) { mostraErro('SEM_EMAIL'); return; }
      texto(erroCpf, '');
      limpaErro();
      pedidoPix = { email: email, cpf: cpf };
      botaoCpf.disabled = true; botaoCpf.setAttribute('aria-busy', 'true');
      envia(montaPedido('bank_transfer', { payment_method_id: 'pix', email: email, cpf: cpf }))
        .then(function () { botaoCpf.disabled = false; botaoCpf.removeAttribute('aria-busy'); });
    });
  }

  /* ---------- 9. Começa ---------- */
  pedeSessao();
})();
