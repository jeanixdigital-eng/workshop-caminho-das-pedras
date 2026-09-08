/* Faixa "versão de trabalho": conta as pendências do próprio DOM.
   🔑 Existe porque número escrito à mão envelhece calado. Em 08/09 a política dizia
   "8 pendências" com 5 no documento e a de obrigado dizia "3" com 1. Quem conta é o DOM. */
(function () {
  'use strict';
  var n = document.getElementById('n-pendencias');
  if (!n) return;
  var total = document.querySelectorAll('.pendente').length;
  n.textContent = String(total);
  var palavra = document.getElementById('n-pendencias-palavra');
  if (palavra) palavra.textContent = total === 1 ? 'pendência' : 'pendências';
})();
