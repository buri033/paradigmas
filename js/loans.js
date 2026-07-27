/**
 * DuckBank - Créditos JS
 */

document.addEventListener('DOMContentLoaded', () => {
  const payQuotaBtn = document.getElementById('payQuotaBtn');
  if (payQuotaBtn) {
    payQuotaBtn.addEventListener('click', () => {
      showToast('Cuota #13 pagada exitosamente por $185.000 CLP', 'success');
    });
  }
});
