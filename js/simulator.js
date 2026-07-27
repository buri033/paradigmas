/**
 * DuckBank - Simulador de Préstamos JS
 */

document.addEventListener('DOMContentLoaded', () => {
  const amountSlider = document.getElementById('amountSlider');
  const termSlider = document.getElementById('termSlider');
  const amountDisplay = document.getElementById('amountDisplay');
  const termDisplay = document.getElementById('termDisplay');
  const monthlyFeeEl = document.getElementById('monthlyFee');
  const totalCostEl = document.getElementById('totalCost');
  const applyBtn = document.getElementById('applySimulatedLoanBtn');

  function calculateLoan() {
    const amount = parseFloat(amountSlider.value);
    const months = parseInt(termSlider.value);

    amountDisplay.textContent = formatCurrency(amount);
    termDisplay.textContent = `${months} meses`;

    // Tasa fija mensual de 1.15% (13.8% anual aproximado)
    const monthlyRate = 0.0115;
    const monthlyFee = (amount * monthlyRate * Math.pow(1 + monthlyRate, months)) / (Math.pow(1 + monthlyRate, months) - 1);
    const totalCost = monthlyFee * months;

    monthlyFeeEl.textContent = formatCurrency(Math.round(monthlyFee));
    totalCostEl.textContent = formatCurrency(Math.round(totalCost));
  }

  if (amountSlider && termSlider) {
    amountSlider.addEventListener('input', calculateLoan);
    termSlider.addEventListener('input', calculateLoan);
    calculateLoan();
  }

  if (applyBtn) {
    applyBtn.addEventListener('click', () => {
      const amount = amountSlider.value;
      window.location.href = `applications.html?product=loan&amount=${amount}`;
    });
  }
});
