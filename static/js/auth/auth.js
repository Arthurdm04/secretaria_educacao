// Criamos um objeto para organizar todas as nossas funções de autenticação
const AuthManager = {
    
    // Pega o token do localStorage
    getToken: function() {
        return localStorage.getItem('accessToken');
    },

    // Verifica se o usuário está logado (se existe um token)
    isLoggedIn: function() {
        return !!this.getToken(); // O '!!' transforma o resultado em um booleano (true/false)
    },

    // Faz o logout do usuário
    logout: function() {
        localStorage.removeItem('accessToken');
        alert('Sua sessão foi encerrada.');
        window.location.href = '/login/'; // Redireciona para a página de login do Django
    },

    /**
     * A função mais importante: um 'fetch' que já inclui o token de autorização
     * e trata automaticamente o erro de token expirado (401).
     * @param {string} url - A URL da API para a qual fazer a requisição.
     * @param {object} options - As mesmas opções que você passaria para o fetch (method, body, etc.).
     * @returns {Promise<Response>} - A promessa da resposta do fetch.
     */
    fetchWithAuth: async function(url, options = {}) {
        const token = this.getToken();
        if (!token) {
            // Se não houver token, não adianta nem tentar. Faz o logout.
            this.logout();
            // Lança um erro para interromper a execução do código que chamou esta função
            throw new Error('Usuário não autenticado.');
        }

        // Prepara os cabeçalhos, adicionando o de Autorização
        const headers = {
            ...options.headers, // Inclui quaisquer outros headers que já existam
            'Authorization': `Bearer ${token}`
        };
        
        // Faz a chamada fetch com os novos cabeçalhos
        const response = await fetch(url, { ...options, headers });

        // Se a resposta for 401 (Não Autorizado), o token expirou ou é inválido
        if (response.status === 401) {
            // Faz o logout e interrompe o fluxo
            this.logout();
            throw new Error('Sessão expirada ou inválida.');
        }

        return response;
    },

    /**
     * Uma função "guarda" para ser chamada no início de cada página protegida.
     */
    protectPage: function() {
        if (!this.isLoggedIn()) {
            alert('Você precisa estar logado para acessar esta página.');
            window.location.href = '/login/';
        }
    }
};