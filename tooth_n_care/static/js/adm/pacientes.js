// Função utilitária para exibir a mensagem de sucesso/erro (em substituição a alert())
function showMessage(type, message) {
    console.log(`[${type.toUpperCase()}]: ${message}`);
    const alertPlaceholder = document.getElementById('content-area');
    if (!alertPlaceholder) return;

    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible fade show fixed-top-0 m-3" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('');

    alertPlaceholder.prepend(wrapper);
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
    const removeButton = document.getElementById('remove-paciente');
    const allCheckbox = document.getElementById('select-all');
    
    // Assegura que haja um delay para o DOM ser totalmente carregado
    setTimeout(() => {
        const checkboxes = document.querySelectorAll('.paciente-checkbox');
        
        // --- Lógica de Habilitar/Desabilitar Botão de Remover ---
        function updateRemoveButtonState() {
            const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
            removeButton.disabled = checkedCount === 0;
            removeButton.textContent = checkedCount > 0 
                ? `Remover Selecionados (${checkedCount})` 
                : 'Remover Selecionados';
        }

        // --- Lógica de Seleção em Massa ---
        allCheckbox.addEventListener('change', (e) => { 
            checkboxes.forEach(cb => cb.checked = e.target.checked);
            updateRemoveButtonState();
        });

        function checkAll() {
            let allChecked = true;
            let checkedCount = 0;
            checkboxes.forEach(cb => {
                if(cb.checked) {
                    checkedCount++;
                } else {
                    allChecked = false;
                }
            });
            
            allCheckbox.checked = allChecked && checkboxes.length > 0;
            updateRemoveButtonState();
        }

        checkboxes.forEach(cb => {
            cb.addEventListener('change', checkAll);
        });

        // Inicializa o estado do botão
        checkAll();
    }, 100); 

    
    // --- Lógica do MODAL de Exclusão e Fetch API ---
    const deleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');

    // 1. Abrir Modal ao clicar em "Remover Selecionados"
    removeButton.addEventListener('click', () => {
        const checkedCount = Array.from(document.querySelectorAll('.paciente-checkbox:checked')).length;

        if(checkedCount === 0) {
            showMessage('warning', 'Selecione pelo menos um paciente para remover.');
            return;
        }

        deleteModal.show();
    });

    // 2. Executar Exclusão ao confirmar no Modal
    confirmDeleteButton.addEventListener('click', () => {
        const csrfToken = getCookie('csrftoken')
        const ids = Array.from(document.querySelectorAll('.paciente-checkbox:checked'))
            .map(cb => parseInt(cb.value));

        console.log(ids);

        deleteModal.hide(); // Fecha o modal imediatamente

        fetch("http://127.0.0.1:8000/deletar-pacientes/", {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ p_ids: ids })
        })
        .then(response => {
            if(!response.ok) return response.json().then(error => { throw new Error(error.mensagem || "Erro inesperado na exclusão."); });
            return response.json();
        })
        .then(data => {
            showMessage('success', data.mensagem || `Exclusão de ${ids.length} paciente(s) realizada com sucesso.`);
            // document.location.reload(); // Recarrega a página após o sucesso
        })
        .catch(error => {
            showMessage('danger', `Falha ao processar a exclusão: ${error.message}`);
            console.error('Falha ao processar a exclusão', error);
        });
    });
});


// --- Lógica do DataTable e Filtro Customizado ---
$(document).ready(function() {
    const tabela = $('#tabela-pacientes').DataTable({
        dom: 'lrtip',
        paging: false,      // desativa paginação
        info: false,        // remove "Mostrando X de Y"
        searching: false,   // desativa o campo de pesquisa interno
        ordering: false,    // Desativa a ordenação clicável nas colunas (A ordenação será feita no JavaScript ou Django)
        columnDefs: [
            { targets: [0, 4], searchable: false } // Impede busca nas colunas de checkbox e ações
        ]
    });

    // Filtra no JavaScript para cada tecla apertada (mantendo a funcionalidade original)
    document.getElementById('searchInput').addEventListener('keyup', function() {
        const termo = $('#searchInput').val().toLowerCase().trim();
        
        tabela.rows().every(function() {
            const rowNode = $(this.node());
            // Usando o atributo data-search definido no HTML
            const dataSearch = rowNode.data('search') || ''; 
            const corresponde = dataSearch.toLowerCase().includes(termo);
            
            rowNode.toggle(corresponde);
        });
    });
});