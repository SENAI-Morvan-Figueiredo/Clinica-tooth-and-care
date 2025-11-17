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
    
    const checkboxes = document.querySelectorAll('.paciente-checkbox');
    
    function updateRemoveButtonState() {
        // Filtra apenas os checkboxes que estão checados E cuja linha pai está visível (se filtrada)
        const checkedCount = Array.from(checkboxes).filter(cb => {
            return cb.checked && $(cb).closest('tr').is(':visible');
        }).length;
        
        removeButton.disabled = checkedCount === 0;
        removeButton.textContent = checkedCount > 0 
            ? `Remover Selecionados (${checkedCount})` 
            : 'Remover Selecionados';
    }

    // --- Lógica de Seleção em Massa ---
    allCheckbox.addEventListener('change', (e) => { 
        // Seleciona/deseleciona apenas os checkboxes em linhas VISÍVEIS
        checkboxes.forEach(cb => {
            if ($(cb).closest('tr').is(':visible')) {
                cb.checked = e.target.checked;
            } else if (e.target.checked === false) {
                 cb.checked = false;
            }
        });
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
    
    // --- Lógica do MODAL de Exclusão e Fetch API ---
    const deleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');

    // Abrir Modal ao clicar em "Remover Selecionados"
    removeButton.addEventListener('click', () => {
        const checkedCount = Array.from(document.querySelectorAll('.paciente-checkbox:checked')).length;

        if(checkedCount === 0) {
            showMessage('warning', 'Selecione pelo menos um paciente para remover.');
            return;
        }

        deleteModal.show();
    });

    confirmDeleteButton.addEventListener('click', () => {
        const csrfToken = getCookie('csrftoken')
        const ids = Array.from(document.querySelectorAll('.paciente-checkbox:checked'))
            .map(cb => parseInt(cb.value));

        deleteModal.hide(); // Fecha o modal imediatamente

        //TODO: modificar a url quando hospedar
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
            document.location.reload(); // Recarrega a página após o sucesso
        })
        .catch(error => {
            showMessage('danger', `Falha ao processar a exclusão: ${error.message}`);
            console.error('Falha ao processar a exclusão', error);
        });
    });
});


$(document).ready(function() {
    const tabelaElementoDOM = document.getElementById('tabela-pacientes');
    const $tabelaElemento = $(tabelaElementoDOM);

    // Verifica se a tabela tem linhas de dados válidas (não apenas a mensagem de 'empty')
    const possuiDados = $tabelaElemento.find('tbody tr:not(.dataTables_empty)').length > 0;
    
    let tabela;

    if (possuiDados) {
        // Inicializa o DataTables APENAS se houver dados
        tabela = $tabelaElemento.DataTable({
            dom: 'lrtip',
            paging: false,
            info: false,
            searching: false,
            ordering: false,
            columnDefs: [
                { targets: [0, 4], searchable: false }
            ]
        });
    } else {
        // Cria um objeto proxy ou trata o caso sem dados para evitar erros no resto do código
        tabela = {
            rows: () => ({ every: () => {} }),
            // Adicione outros métodos mockados (como .rows().every) que você usa abaixo
        };
    }

    let debounceTimer; // Variável para controlar o debounce

    function aplicarFiltro() {
        const termo = $('#searchInput').val().toLowerCase().trim();
        
        tabela.rows().every(function() {
            const rowNode = $(this.node());
            // Pega o valor do atributo data-search definido no HTML
            const dataSearch = rowNode.data('search') || ''; 
            const corresponde = dataSearch.toLowerCase().includes(termo);
            
            rowNode.toggle(corresponde);
        });

        if (typeof checkAll === "function") {
            checkAll();
        }
    }

    // Aplica a otimização de Debounce ao evento keyup
    document.getElementById('searchInput').addEventListener('keyup', function() {
        clearTimeout(debounceTimer); 
        debounceTimer = setTimeout(aplicarFiltro, 300); 
    });
});