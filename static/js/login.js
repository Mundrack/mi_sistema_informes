document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const messageElement = document.getElementById('message');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nombre_usuario: username, contrasena: password })
        });

        const data = await response.json();

        if (response.ok) {
            messageElement.style.color = 'green';
            messageElement.textContent = '¡Login exitoso! Redirigiendo...';
            // Aquí, en un sistema real, guardaríamos un token y redirigiríamos.
            // Por ahora, solo te mostraremos el mensaje de éxito.
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1500);
        } else {
            messageElement.style.color = 'red';
            messageElement.textContent = data.error;
        }
    });
});