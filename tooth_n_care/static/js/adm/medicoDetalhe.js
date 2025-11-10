document.addEventListener('DOMContentLoaded', () => {
    const deleteButton = document.getElementById('delete-medico-button');
    const deleteModalElement = document.getElementById('confirmDeleteModal');
    
    // Verifica se os elementos necessários existem
    if (!deleteButton || !deleteModalElement) {
        console.error("Elementos necessários para a lógica de exclusão não foram encontrados.");
        return;
    }
    
    // Inicializa o modal do Bootstrap
    const deleteModal = new bootstrap.Modal(deleteModalElement);
    const medicoNomePlaceholder = document.getElementById('medicoNomePlaceholder');

    // 1. Abrir Modal ao clicar em "Deletar Médico"
    deleteButton.addEventListener('click', () => {
        const medicoNome = deleteButton.getAttribute('data-medico-nome');
        
        // Atualiza o nome do médico no corpo do modal
        if (medicoNomePlaceholder) {
            medicoNomePlaceholder.textContent = medicoNome;
        }

        deleteModal.show();
    });
});