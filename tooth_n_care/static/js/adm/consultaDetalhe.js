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
    
    const deleteModal = new bootstrap.Modal(deleteModalElement);
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');
    const consultaDataPlaceholder = document.getElementById('consultaDataPlaceholder');
    const consultaIdPlaceholder = document.getElementById('consultaIdPlaceholder');

    // 1. Preencher Modal ao ser exibido
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

    // 2. Executar Exclusão ao confirmar
    confirmDeleteButton.addEventListener('click', () => {
        const deleteUrl = confirmDeleteButton.getAttribute('data-delete-url');
        
        // Obtém o token CSRF do DOM
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

        if (!csrfToken || !deleteUrl) {
            showMessage('danger', 'Erro: Falta o token de segurança ou a URL de exclusão.');
            deleteModal.hide();
            return;
        }

        deleteModal.hide(); 

        fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        })
        .then(response => {
            if (response.status === 204) {
                 // 204 No Content é sucesso sem corpo de resposta
                return { mensagem: "Consulta deletada com sucesso." }; 
            }
            if (!response.ok) {
                // Tenta ler o erro do corpo da resposta, se disponível
                return response.json().then(error => { 
                    throw new Error(error.mensagem || `Erro ${response.status}: Falha inesperada na exclusão.`); 
                });
            }
            return response.json(); 
        })
        .then(data => {
            showMessage('success', data.mensagem || 'Consulta deletada com sucesso. Redirecionando...');
            
            // Redireciona para a lista de consultas
            setTimeout(() => {
                // ATENÇÃO: Em um ambiente Django, você deve usar a tag {% url 'adm-consultas' %}
                // Aqui usamos um path hardcoded como exemplo.
                window.location.href = "/adm/consultas"; 
            }, 1500);
        })
        .catch(error => {
            showMessage('danger', `Falha ao processar a exclusão: ${error.message}`);
            console.error('Falha ao processar a exclusão', error);
        });
    });
});