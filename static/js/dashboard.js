// Em static/js/dashboard.js

// Espera o conteúdo da página carregar
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. CHAMA O NOSSO "GUARDA" DE PÁGINA
    AuthManager.protectPage();

    const userInfoDiv = document.getElementById('user-info');

    // 2. USA NOSSO 'fetch' PERSONALIZADO PARA BUSCAR OS DADOS
    AuthManager.fetchWithAuth('http://localhost:8000/users/me')
        .then(response => {
            // Se a requisição chegar aqui, ela foi bem-sucedida (não deu erro 401)
            if (!response.ok) {
                // Trata outros erros de servidor (ex: 500)
                throw new Error(`Erro na API: ${response.statusText}`);
            }
            return response.json();
        })
        .then(userData => {
            // 3. ATUALIZA A PÁGINA COM OS DADOS
            userInfoDiv.innerHTML = `
                <p><strong>ID do Usuário:</strong> ${userData.id}</p>
                <p><strong>Nome:</strong> ${userData.full_name}</p>
                <p><strong>Email:</strong> ${userData.email}</p>
                <p><strong>Cargo:</strong> ${userData.role}</p>
            `;
        })
        .catch(error => {
            // O catch agora pega tanto erros de rede quanto os erros que lançamos
            // no fetchWithAuth (token expirado, etc.). A lógica de redirect já
            // foi cuidada lá dentro.
            console.error('Falha ao buscar dados do usuário:', error);
            if (userInfoDiv) {
                userInfoDiv.innerHTML = `<p style="color: red;">Não foi possível carregar os dados do usuário.</p>`;
            }
        });

    // // 4. A LÓGICA DE LOGOUT AGORA CHAMA A FUNÇÃO CENTRALIZADA
    // document.getElementById('logout-button').addEventListener('click', () => {
    //     AuthManager.logout();
    // });
});