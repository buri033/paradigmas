/**
 * DuckBank - Auth Logic (Login, Register, Forgot Password)
 */

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const forgotForm = document.getElementById('forgotForm');

  // Login Handler
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      if (!email || !password) {
        showToast('Por favor completa todos los campos', 'error');
        return;
      }

      // Simular login exitoso
      const mockUser = {
        name: email.split('@')[0].toUpperCase() || 'Usuario DuckBank',
        email: email
      };
      localStorage.setItem('duckbank_user', JSON.stringify(mockUser));
      showToast('¡Sesión iniciada con éxito! Redirigiendo...', 'success');

      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1200);
    });
  }

  // Register Handler
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('fullName').value;
      const email = document.getElementById('regEmail').value;
      const pass = document.getElementById('regPassword').value;
      const terms = document.getElementById('terms').checked;

      if (!name || !email || !pass) {
        showToast('Por favor completa todos los campos requeridos', 'error');
        return;
      }

      if (!terms) {
        showToast('Debes aceptar los términos y condiciones', 'error');
        return;
      }

      const newUser = { name: name, email: email };
      localStorage.setItem('duckbank_user', JSON.stringify(newUser));
      showToast('¡Cuenta registrada con éxito! Bienvenido a DuckBank', 'success');

      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1500);
    });
  }

  // Forgot Password Handler
  if (forgotForm) {
    forgotForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('forgotEmail').value;

      if (!email) {
        showToast('Ingresa tu correo electrónico registrado', 'error');
        return;
      }

      showToast(`Enlace de recuperación enviado a ${email}`, 'success');
      setTimeout(() => {
        window.location.href = 'login.html';
      }, 2000);
    });
  }
});
