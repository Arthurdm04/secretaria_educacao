function togglePassword() {
    const senha = document.getElementById('senha');
    if (senha.type === 'password') {
        senha.type = 'text';
    } else {
        senha.type = 'password';
    }
}

// Espera o conteúdo da página carregar completamente antes de executar o script
document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.querySelector('#login-form');
    const emailInput = document.querySelector('#email');
    const passwordInput = document.querySelector('#senha');
    const messageArea = document.querySelector('#message-area');

    // Adiciona um "escutador" para o evento de submissão do formulário
    loginForm.addEventListener('submit', async (event) => {
        // Previne o comportamento padrão do formulário, que é recarregar a página
        event.preventDefault();

        // Limpa mensagens de erro anteriores
        messageArea.innerText = '';

        // Pega os valores digitados pelo usuário
        const email = emailInput.value;
        const password = passwordInput.value;

        // Monta o corpo da requisição no formato x-www-form-urlencoded
        // A API espera 'username', então mapeamos nosso 'email' para 'username'
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        try {
            // Envia a requisição para a API FastAPI
            // Lembre-se de que o Django e o FastAPI rodam em portas diferentes
            const response = await fetch('http://127.0.0.1:8000/login/token', {
                method: 'POST',
                body: formData
            });

            // Converte a resposta em JSON
            const data = await response.json();

            // Se a resposta for bem-sucedida (status 200-299)
            if (response.ok) {
                // Armazena o token no localStorage do navegador
                localStorage.setItem('accessToken', data.access_token);
                
                // Dá um feedback visual para o usuário
                messageArea.style.color = 'green';
                messageArea.innerText = 'Login bem-sucedido! Redirecionando...';

                // Redireciona para a página de dashboard após 1 segundo
                setTimeout(() => {
                    // Substitua '/dashboard' pela URL da sua página principal no Django
                    window.location.href = '/dashboard/'; 
                }, 1000);

            } else {
                // Se a resposta for um erro (401, etc.), mostra o detalhe do erro
                messageArea.style.color = 'red';
                messageArea.innerText = data.detail || 'Ocorreu um erro.';
            }

        } catch (error) {
            // Trata erros de rede (API fora do ar, etc.)
            messageArea.style.color = 'red';
            messageArea.innerText = 'Não foi possível conectar com o servidor.';
            console.error('Erro de conexão:', error);
        }
    });
});

