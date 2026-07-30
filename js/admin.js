/**
 * DuckBank - Panel del Admin JS
 */

document.addEventListener('DOMContentLoaded', () => {
  const approveBtns = document.querySelectorAll('.approveBtn');
  const rejectBtns = document.querySelectorAll('.rejectBtn');

  approveBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const row = btn.closest('tr');
      const statusBadge = row.querySelector('.badge');
      statusBadge.className = 'badge badge-success';
      statusBadge.textContent = 'Aprobado';
      showToast('Solicitud aprobada exitosamente', 'success');
    });
  });

  rejectBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const row = btn.closest('tr');
      const statusBadge = row.querySelector('.badge');
      statusBadge.className = 'badge badge-warning';
      statusBadge.textContent = 'Rechazado';
      showToast('Solicitud rechazada', 'error');
    });
  });
});
