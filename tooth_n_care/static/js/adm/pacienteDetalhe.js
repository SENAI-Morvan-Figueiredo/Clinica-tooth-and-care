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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // O nome 'csrftoken' começa com este prefixo?
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    const deleteButton = document.getElementById('remove-paciente');
    const deleteModalElement = document.getElementById('confirmDeleteModal');
    
    // Verifica se os elementos necessários existem
    if (!deleteButton || !deleteModalElement) {
        // Se estiver faltando, apenas loga e sai, não precisa de showMessage aqui
        console.error("Elementos necessários para a lógica de exclusão não foram encontrados.");
        return;
    }
    
    // Inicializa o modal do Bootstrap
    const deleteModal = new bootstrap.Modal(deleteModalElement);
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

});