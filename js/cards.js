/**
 * DuckBank - Tarjetas de Crédito JS
 */

document.addEventListener('DOMContentLoaded', () => {
  const toggleCvvBtn = document.getElementById('toggleCvvBtn');
  const cvvText = document.getElementById('cvvText');
  const lockBtn = document.getElementById('lockBtn');
  const payCardBtn = document.getElementById('payCardBtn');

  if (toggleCvvBtn && cvvText) {
    let visible = false;
    toggleCvvBtn.addEventListener('click', () => {
      visible = !visible;
      cvvText.textContent = visible ? '842' : '•••';
      toggleCvvBtn.textContent = visible ? 'Ocultar CVV' : 'Ver CVV';
    });
  }

  if (lockBtn) {
    let locked = false;
    lockBtn.addEventListener('click', () => {
      locked = !locked;
      if (locked) {
        lockBtn.classList.remove('btn-outline');
        lockBtn.classList.add('btn-danger');
        lockBtn.textContent = '🔒 Tarjeta Bloqueada';
        showToast('Tarjeta bloqueada temporalmente por seguridad', 'error');
      } else {
        lockBtn.classList.remove('btn-danger');
        lockBtn.classList.add('btn-outline');
        lockBtn.textContent = '🔓 Desbloquear Tarjeta';
        showToast('Tarjeta desbloqueada exitosamente', 'success');
      }
    });
  }

  if (payCardBtn) {
    payCardBtn.addEventListener('click', () => {
      showToast('Pago de tarjeta procesado por $340.000 CLP', 'success');
    });
  }
});
