document.addEventListener('DOMContentLoaded', () => {
    // Lógica de autenticação e busca de dados do professor (se necessário)
    AuthManager.protectPage();
    const userInfoDiv = document.getElementById('user-info');
    AuthManager.fetchWithAuth('http://localhost:8000/users/me')
        .then(response => response.json())
        .then(professorData => {
            if (userInfoDiv) {
                userInfoDiv.innerHTML = `<p><strong>${professorData.full_name || 'Professor'}</strong></p><p>${professorData.role || ''}</p>`;
            }
        }).catch(console.error);

    // Lógica para controle das abas
    const tabs = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove a classe 'active' de todas as abas e conteúdos
            tabs.forEach(item => item.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Adiciona a classe 'active' na aba clicada e no conteúdo correspondente
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
        });
    });

    // Simulando o envio de formulários com alertas
    document.querySelectorAll('.btn-primary').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault(); // Impede o envio real do formulário
            const parentTab = button.closest('.tab-content').id;
            let message = '';

            switch (parentTab) {
                case 'notas':
                    message = 'Notas salvas com sucesso!';
                    break;
                case 'presenca':
                    message = 'Presenças registradas com sucesso!';
                    break;
                case 'relatorios':
                    message = 'Relatório gerado com sucesso!';
                    // Aqui você implementaria a lógica para exibir o relatório
                    break;
                case 'avisos':
                    const turma = document.getElementById('turma-aviso').value;
                    const aviso = document.getElementById('mensagem-aviso').value;
                    if (!turma || !aviso) {
                        alert('Por favor, selecione a turma e digite uma mensagem.');
                        return;
                    }
                    message = `Aviso enviado para a turma ${turma}!`;
                    document.getElementById('mensagem-aviso').value = ''; // Limpa o campo
                    break;
                default:
                    message = 'Ação realizada com sucesso!';
            }
            alert(message);
        });
    });

    // Preenche a data de hoje no campo de presença
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('data-presenca').value = today;
});