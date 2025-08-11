document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
  
    registerForm.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const email = document.getElementById('register-email').value;
      const password = document.getElementById('register-password').value;
  
      const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
  
      const result = await response.json();
  
      if (response.ok) {
        alert(result.message);
        window.location.href = '/';
      } else {
        alert(result.message);
      }
    });
  });
  