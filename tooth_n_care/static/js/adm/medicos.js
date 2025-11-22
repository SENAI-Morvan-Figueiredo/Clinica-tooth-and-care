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
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('DOMContentLoaded', () => {
    const removeButton = document.getElementById('remove-medico');
    const deactBtn = document.getElementById('desativa-btn');
    const allCheckbox = document.getElementById('select-all');
    
    const checkboxes = document.querySelectorAll('.medico-checkbox');
    
    // --- Lógica de Habilitar/Desabilitar Botão de Remover ---
    function updateButtons() {
        const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
        removeButton.disabled = checkedCount === 0;
        removeButton.textContent = checkedCount > 0 
            ? `Remover Selecionados (${checkedCount})` 
            : 'Remover Selecionados';

        deactBtn.disabled = checkedCount === 0;
        deactBtn.textContent = checkedCount > 0
            ? `Desativar Selecionados (${checkedCount})`
            : 'Desativar Selecionados';
    }

    // --- Lógica de Seleção em Massa ---
    allCheckbox.addEventListener('change', (e) => { 
        checkboxes.forEach(cb => cb.checked = e.target.checked);
        updateButtons();
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
        updateButtons();
    }

    checkboxes.forEach(cb => {
        cb.addEventListener('change', checkAll);
    });

    checkAll();

    window.checkAll = checkAll;

    // --- Lógica do MODAL de Exclusão e Fetch API ---
    const deleteModalElement = document.getElementById('confirmDeleteModal');
    if (!deleteModalElement) return; // Garante que o modal existe
    
    const deleteModal = new bootstrap.Modal(deleteModalElement);
    const deleteMessage = document.getElementById('deleteMessage');
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');

    removeButton.addEventListener('click', () => {
        const checkedCount = Array.from(document.querySelectorAll('.medico-checkbox:checked')).length;

        if(checkedCount === 0) {
            showMessage('warning', 'Selecione pelo menos um médico para remover.');
            return;
        }

        deleteMessage.innerHTML = `Você está prestes a deletar <strong>${checkedCount}</strong> médico(s) selecionado(s).`;
        deleteModal.show();
    });

    const deactModalElement = document.getElementById('confirmDeactModal');
    if (!deactModalElement) return; // Garante que o modal existe

    const deactModal = new bootstrap.Modal(deactModalElement);
    const deactMessage = document.getElementById('deactMessage');
    const confirmDeactButton = document.getElementById('confirmDeactButton');

    deactBtn.addEventListener('click', () => {
        const checkedCount = Array.from(document.querySelectorAll('.medico-checkbox:checked')).length;

        if(checkedCount === 0) {
            showMessage('warning', 'Selecione pele menos um médico para desativar.');
            return;
        }

        deactMessage.innerHTML = `Você está preses a desativar <strong>${checkedCount}</strong> médico(s) selecionado(s).`;
        deactModal.show();
    });

    // função para enviar a requisição ao back
    function processarAcao(ids, url, actionName) {
        const csrfToken = getCookie('csrftoken');

        if (!csrfToken) {
            showMessage('danger', 'Token CSRF não encontrado. Falha de segurança.');
            console.error('CSRF Token missing.');
            deleteModal.hide();
            return;
        }

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ medico_ids: ids })
        })
        .then(response => {
            if(!response.ok) return response.json().then(error => { throw new Error(error.mensagem || "Erro inesperado na exclusão."); });
            return response.json();
        })
        .then(data => {
            document.location.reload(); // Recarrega a página após o sucesso
        })
        .catch(error => {
            showMessage('danger', `Falha ao processar a ${actionName}: ${error.message}`);
            console.error(`Falha ao processar a ${actionName}`, error);
        });
    }

    confirmDeleteButton.addEventListener('click', () => {
        const ids = Array.from(document.querySelectorAll('.medico-checkbox:checked'))
            .map(cb => parseInt(cb.value));

        deleteModal.hide();
        processarAcao(ids, '/deletar-medicos', 'Deletar');
    });
    confirmDeactButton.addEventListener('click', () => {
        const ids = Array.from(document.querySelectorAll('.medico-checkbox:checked'))
            .map(cb => parseInt(cb.value));

        deactModal.hide();
        processarAcao(ids, '/desativar-medicos', 'Desativar')
    });
});

// ------------------- DataTables --------------------
$(document).ready(function() {
    const tabelaElementoDOM = document.getElementById('tabela-medicos');
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