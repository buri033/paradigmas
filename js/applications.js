/**
 * DuckBank - Solicitud de Productos JS
 */

document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.product-option-card');
  const appForm = document.getElementById('productAppForm');
  const selectedProductTitle = document.getElementById('selectedProductTitle');
  let currentProduct = 'Tarjeta de Crédito Duck Visa';

  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      currentProduct = card.dataset.product;
      selectedProductTitle.textContent = currentProduct;
    });
  });

  if (appForm) {
    appForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const income = document.getElementById('monthlyIncome').value;

      if (!income) {
        showToast('Por favor indica tus ingresos mensuales', 'error');
        return;
      }

      showToast(`¡Solicitud enviada para "${currentProduct}"! Te evaluaremos en 24h.`, 'success');
      appForm.reset();
    });
  }
});
