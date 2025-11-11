// Função utilitária para exibir a mensagem de sucesso/erro
function showMessage(type, message) {
    console.log(`[${type.toUpperCase()}]: ${message}`);
    
    const alertPlaceholder = document.getElementById('content-area');
    if (!alertPlaceholder) return;

    // Cria o Alerta/Toast do Bootstrap no topo
    const wrapper = document.createElement('div');
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
    const deleteButton = document.getElementById('delete-consulta-button');
    const deleteModalElement = document.getElementById('confirmDeleteModal');
    
    if (!deleteButton || !deleteModalElement) {
        console.error("Elementos necessários (botão/modal) não foram encontrados.");
        return;
    }
    
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');
    const consultaDataPlaceholder = document.getElementById('consultaDataPlaceholder');
    const consultaIdPlaceholder = document.getElementById('consultaIdPlaceholder');

    deleteModalElement.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget;
        const consultaId = button.getAttribute('data-consulta-id');
        const consultaData = button.getAttribute('data-consulta-data');
        const deleteUrl = button.getAttribute('data-delete-url');

        // Atualiza os placeholders no corpo do modal
        if (consultaDataPlaceholder) {
            consultaDataPlaceholder.textContent = consultaData;
        }
        if (consultaIdPlaceholder) {
            consultaIdPlaceholder.textContent = consultaId;
        }

        // Armazena a URL de delete no botão de confirmação
        confirmDeleteButton.setAttribute('data-delete-url', deleteUrl);
    });
});