/**
 * DuckBank - Dashboard Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // Animación suave de balance al cargar
  const balanceEl = document.getElementById('mainBalance');
  if (balanceEl) {
    animateValue(balanceEl, 0, 4850900, 1000);
  }
});

function animateValue(obj, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const current = Math.floor(progress * (end - start) + start);
    obj.innerHTML = formatCurrency(current);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}
