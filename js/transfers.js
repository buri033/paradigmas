/**
 * DuckBank - Transferencias JS
 */

document.addEventListener('DOMContentLoaded', () => {
  const transferForm = document.getElementById('transferForm');
  const contacts = document.querySelectorAll('.contact-avatar-item');
  const modal = document.getElementById('successModal');
  const closeModalBtn = document.getElementById('closeModalBtn');

  // Selección de contacto rápido
  contacts.forEach(contact => {
    contact.addEventListener('click', () => {
      contacts.forEach(c => c.classList.remove('selected'));
      contact.classList.add('selected');

      const name = contact.dataset.name;
      const bank = contact.dataset.bank;
      const rut = contact.dataset.rut;
      const account = contact.dataset.account;

      document.getElementById('destName').value = name;
      document.getElementById('destBank').value = bank;
      document.getElementById('destRut').value = rut;
      document.getElementById('destAccount').value = account;

      showToast(`Contacto ${name} seleccionado`, 'success');
    });
  });

  // Envío del formulario
  if (transferForm) {
    transferForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const amount = document.getElementById('transferAmount').value;
      const destName = document.getElementById('destName').value;

      if (!amount || amount <= 0) {
        showToast('Ingresa un monto válido para transferir', 'error');
        return;
      }

      // Rellenar comprobante modal
      document.getElementById('receiptAmount').textContent = formatCurrency(amount);
      document.getElementById('receiptDest').textContent = destName;
      document.getElementById('receiptDate').textContent = new Date().toLocaleString('es-CL');

      // Mostrar modal
      modal.classList.add('active');
    });
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => {
      modal.classList.remove('active');
      transferForm.reset();
      contacts.forEach(c => c.classList.remove('selected'));
    });
  }
});
