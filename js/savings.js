/**
 * DuckBank - Cuenta de Ahorros JS
 */

document.addEventListener('DOMContentLoaded', () => {
  const goalForm = document.getElementById('addGoalForm');
  
  if (goalForm) {
    goalForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const title = document.getElementById('goalTitle').value;
      const target = document.getElementById('goalTarget').value;

      if (!title || !target) {
        showToast('Completa los datos de la meta', 'error');
        return;
      }

      showToast(`¡Meta "${title}" creada con éxito!`, 'success');
      goalForm.reset();
    });
  }
});
