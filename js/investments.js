/**
 * DuckBank - Inversiones JS
 */

document.addEventListener('DOMContentLoaded', () => {
  const investButtons = document.querySelectorAll('.investBtn');
  
  investButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const fundName = btn.dataset.fund;
      showToast(`Inversión iniciada en ${fundName}. ¡Felicidades!`, 'success');
    });
  });
});
