/* Página de venda do Workshop · assets/pagina.js · só o index.html usa.
   Contrato: rascunho/estrutura.md §2 (formulário), §3.6 (barra fixa), §5 (rastreio).
   Sem JavaScript a página continua funcionando: o formulário posta pelo `action` e o `required` nativo segura vazio. */
(function () {
  'use strict';

  var form = document.getElementById('form-inscricao');
  var botao = form ? form.querySelector('button[type="submit"]') : null;
  var bloco = document.getElementById('form-erro');
  var ok = document.getElementById('form-ok');

  /* ---------- Faixa "versão de trabalho": conta as pendências que estão no DOM ---------- */
  var n = document.getElementById('n-pendencias');
  if (n) n.textContent = String(document.querySelectorAll('.pendente').length);

  /* ---------- UTM / fbclid → campos escondidos; pagina = URL sem a query ---------- */
  if (form) {
    var q = new URLSearchParams(location.search);
    ['utm_source', 'utm_medium', 'utm_campaign', 'fbclid'].forEach(function (k) {
      if (form.elements[k]) form.elements[k].value = q.get(k) || '';
    });
    if (form.elements.pagina) form.elements.pagina.value = location.href.replace(/[?#].*$/, '');
  }

  /* ---------- Máscara de telefone: só formata, nunca recusa (§2.7, espelha o e164br do servidor) ---------- */
  var tel = form ? form.elements.telefone : null;
  if (tel) {
    tel.addEventListener('input', function () {
      var d = tel.value.replace(/\D/g, '');
      if ((d.length === 12 || d.length === 13) && d.indexOf('55') === 0) d = d.slice(2);
      d = d.replace(/^0+/, '').slice(0, 11);
      tel.value = d.length > 10 ? d.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3')
               : d.length > 6  ? d.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3')
               : d.length > 2  ? d.replace(/^(\d{2})(\d{0,5})/, '($1) $2') : d;
    });
  }

  /* ---------- Mensagens (copy.md, bloco FORMULÁRIO): [campo, texto]; campo null = erro de bloco ---------- */
  var MSG = {
    NOME_OBRIGATORIO:  ['nome', 'Preciso do seu nome para registrar a inscrição.'],
    TELEFONE_INVALIDO: ['telefone', 'Esse número não passou. Confira o DDD e os dígitos do seu WhatsApp.'],
    DDD_INVALIDO:      ['telefone', 'Esse número não passou. Confira o DDD e os dígitos do seu WhatsApp.'],
    EMAIL_INVALIDO:    ['email', 'Esse e-mail não passou. Confira se está completo, com o @ e o ponto.'],
    SEM_CONSENTIMENTO: ['consentimento', 'Sem a sua autorização eu não posso guardar o seu contato nem te mandar o link. Marque a caixa para seguir.'],
    MUITAS_TENTATIVAS: [null, 'Foram muitos envios seguidos daqui. Espere uma hora e tente de novo.'],
    FUNIL_INDISPONIVEL: [null, 'A inscrição não passou agora, e o problema é do nosso lado, não seu. Tente de novo em alguns minutos. Se continuar, me chama no direct do @dieymisson_.']
  };
  var CAMPOS = ['nome', 'telefone', 'email', 'consentimento'];

  function limpaErros() {
    CAMPOS.forEach(function (c) {
      var el = form.elements[c], erro = document.getElementById('erro-' + c);
      if (el) { el.removeAttribute('aria-invalid'); el.removeAttribute('aria-describedby'); }
      if (erro) erro.textContent = '';
    });
    bloco.textContent = '';
  }

  /* Texto de bloco; "@dieymisson_" vira link para o Instagram (§2.5) */
  function textoComLink(texto) {
    var alvo = '@dieymisson_', i = texto.indexOf(alvo), frag = document.createDocumentFragment();
    if (i < 0) { frag.appendChild(document.createTextNode(texto)); return frag; }
    frag.appendChild(document.createTextNode(texto.slice(0, i)));
    var a = document.createElement('a');
    a.href = 'https://www.instagram.com/dieymisson_/'; a.target = '_blank'; a.rel = 'noopener'; a.textContent = alvo;
    frag.appendChild(a);
    frag.appendChild(document.createTextNode(texto.slice(i + alvo.length)));
    return frag;
  }

  /* Um erro novo apaga o anterior. Vários códigos de campo de uma vez (validação local); o foco vai para o primeiro. */
  function mostraErros(codigos) {
    limpaErros();
    var primeiro = null;
    codigos.forEach(function (codigo) {
      var m = MSG[codigo] || MSG.FUNIL_INDISPONIVEL, campo = m[0], texto = m[1];
      if (!campo) { bloco.textContent = ''; bloco.appendChild(textoComLink(texto)); return; }
      var el = form.elements[campo], erro = document.getElementById('erro-' + campo);
      erro.textContent = texto;
      el.setAttribute('aria-invalid', 'true');
      el.setAttribute('aria-describedby', erro.id);
      if (!primeiro) primeiro = el;
    });
    if (primeiro) primeiro.focus();
  }
  function mostraErro(codigo) { mostraErros([codigo]); }

  /* Só vazio e aceite (§2.6): formato de telefone e e-mail é régua do servidor */
  function validaLocal() {
    var e = form.elements, faltas = [];
    if (!e.nome.value.trim()) faltas.push('NOME_OBRIGATORIO');
    if (!e.telefone.value.trim()) faltas.push('TELEFONE_INVALIDO');
    if (!e.email.value.trim()) faltas.push('EMAIL_INVALIDO');
    if (!e.consentimento.checked) faltas.push('SEM_CONSENTIMENTO');
    if (faltas.length) { mostraErros(faltas); return false; }
    return true;
  }

  /* 200 {ok:true,next}: some o formulário, mensagem de sucesso, Lead no pixel, 400 ms, redireciona (§2.5) */
  function sucesso(next) {
    var nome = form.elements.nome.value.trim().split(/\s+/)[0];
    form.hidden = true;
    var p = document.createElement('p');
    p.textContent = 'Recebi, ' + nome + '. Agora é o pagamento: R$ 97, Pix ou cartão. Estou te levando para lá.';
    ok.textContent = '';
    ok.appendChild(p);
    var a = document.createElement('a');
    a.className = 'cta'; a.href = next; a.textContent = 'Ir para o pagamento';
    ok.appendChild(a);
    if (typeof window.fbq === 'function') window.fbq('track', 'Lead');
    setTimeout(function () { location.assign(next); }, 400);
  }

  /* ---------- Envio: requisição simples de CORS, sem header manual, timeout de 20 s (§2.4) ---------- */
  if (form) {
    form.noValidate = true;
    CAMPOS.forEach(function (c) {
      var el = form.elements[c];
      if (el) el.addEventListener(c === 'consentimento' ? 'change' : 'input', function () {
        if (el.getAttribute('aria-invalid')) {
          el.removeAttribute('aria-invalid'); el.removeAttribute('aria-describedby');
          document.getElementById('erro-' + c).textContent = '';
        }
      });
    });

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!validaLocal()) return;
      limpaErros();
      botao.disabled = true; botao.setAttribute('aria-busy', 'true');
      var ctrl = new AbortController();
      var t = setTimeout(function () { ctrl.abort(); }, 20000);
      fetch(form.action, { method: 'POST', body: new URLSearchParams(new FormData(form)), signal: ctrl.signal })
        .then(function (r) {
          return r.json().catch(function () { return null; }).then(function (j) {
            if (r.ok && j && j.ok === true) {
              /* só redireciona para https:// (defesa contra javascript:); sem `next` a copy não tem texto: usa "Funil indisponível" */
              if (typeof j.next === 'string' && j.next.indexOf('https://') === 0) return sucesso(j.next);
              return mostraErro('FUNIL_INDISPONIVEL');
            }
            mostraErro((j && j.codigo) || (r.status === 429 ? 'MUITAS_TENTATIVAS' : 'FUNIL_INDISPONIVEL'));
          });
        })
        .catch(function () { mostraErro('FUNIL_INDISPONIVEL'); })
        .then(function () {
          clearTimeout(t);
          botao.disabled = false; botao.removeAttribute('aria-busy');
        });
    });
  }

  /* ---------- Barra fixa de CTA no celular (§3.6): aparece quando o botão do hero sai, some com a inscrição à vista ---------- */
  var barra = document.getElementById('barra-cta');
  var heroCta = document.getElementById('cta-hero');
  var inscricao = document.getElementById('inscricao');
  if (barra && heroCta && inscricao && 'IntersectionObserver' in window) {
    var heroFora = false, inscricaoVisivel = false;
    var atualiza = function () { barra.classList.toggle('visivel', heroFora && !inscricaoVisivel); };
    new IntersectionObserver(function (es) { heroFora = !es[es.length - 1].isIntersecting; atualiza(); }).observe(heroCta);
    new IntersectionObserver(function (es) { inscricaoVisivel = es[es.length - 1].isIntersecting; atualiza(); }).observe(inscricao);
  }

  /* ---------- Pixel da Meta: só com data-pixel-id preenchido (§5). Hoje vazio: nenhuma requisição sai daqui ---------- */
  (function () {
    var id = document.body.dataset.pixelId;
    if (!id) return;
    /* código-base oficial do pixel (fbevents.js), sem alteração */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', id); window.fbq('track', 'PageView');
  })();
})();
