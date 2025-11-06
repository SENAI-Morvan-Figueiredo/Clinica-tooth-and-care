// Função utilitária para exibir a mensagem de sucesso/erro (em substituição a alert())
function showMessage(type, message) {
    // Implementar aqui uma função para exibir mensagens na UI (ex: Toast do Bootstrap)
    console.log(`[${type.toUpperCase()}]: ${message}`);
    
    const alertPlaceholder = document.getElementById('content-area');
    if (!alertPlaceholder) return;

    // Cria o Toast/Alerta no topo
    const wrapper = document.createElement('div');
    // Usando classes do Bootstrap para Alerta e fixando o estilo no topo
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible fade show fixed-top-0 m-3" role="alert" style="z-index: 1050; position: fixed;">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('');

    alertPlaceholder.prepend(wrapper);
    // Remove o alerta automaticamente após 5 segundos
    setTimeout(() => wrapper.remove(), 5000);
}


document.addEventListener('DOMContentLoaded', () => {
    const deleteButton = document.getElementById('delete-paciente-button');
    const deleteModalElement = document.getElementById('confirmDeleteModal');
    
    // Verifica se os elementos necessários existem
    if (!deleteButton || !deleteModalElement) {
        // Se estiver faltando, apenas loga e sai, não precisa de showMessage aqui
        console.error("Elementos necessários para a lógica de exclusão não foram encontrados.");
        return;
    }
    
    // Inicializa o modal do Bootstrap
    const deleteModal = new bootstrap.Modal(deleteModalElement);
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');
    const pacienteNomePlaceholder = document.getElementById('pacienteNomePlaceholder');

    // 1. Abrir Modal ao clicar em "Deletar Paciente"
    deleteButton.addEventListener('click', () => {
        const pacienteNome = deleteButton.getAttribute('data-paciente-nome');
        
        // Atualiza o nome do paciente no corpo do modal
        if (pacienteNomePlaceholder) {
            pacienteNomePlaceholder.textContent = pacienteNome;
        }

        deleteModal.show();
    });

    // 2. Executar Exclusão ao confirmar no Modal
    confirmDeleteButton.addEventListener('click', () => {
        const deleteUrl = deleteButton.getAttribute('data-delete-url');
        
        // Obtém o token CSRF do DOM
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

        if (!csrfToken) {
            showMessage('danger', 'Token CSRF não encontrado. Falha de segurança.');
            console.error('CSRF Token missing.');
            deleteModal.hide();
            return;
        }

        deleteModal.hide(); // Fecha o modal imediatamente

        fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            // Não precisamos de body, a URL já carrega o ID do paciente
        })
        .then(response => {
            if (response.status === 204) {
                 // Resposta 204 (No Content) é comum para exclusão bem-sucedida sem retorno de JSON
                return { mensagem: "Paciente deletado com sucesso." };
            }
            if (!response.ok) {
                return response.json().then(error => { 
                    throw new Error(error.mensagem || `Erro ${response.status}: Falha inesperada na exclusão.`); 
                });
            }
            return response.json();
        })
        .then(data => {
            // O paciente foi excluído, redirecionamos para a lista de pacientes
            showMessage('success', data.mensagem || 'Paciente deletado com sucesso. Redirecionando...');
            
            // Redireciona após um pequeno delay para que a mensagem seja visível
            setTimeout(() => {
                // Assume que a URL 'adm-pacientes' é a lista de pacientes
                window.location.href = "{% url 'adm-pacientes' %}"; 
            }, 1500);
        })
        .catch(error => {
            showMessage('danger', `Falha ao processar a exclusão: ${error.message}`);
            console.error('Falha ao processar a exclusão', error);
        });
    });
});