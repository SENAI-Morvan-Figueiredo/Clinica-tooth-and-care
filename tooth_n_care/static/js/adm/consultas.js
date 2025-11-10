$(document).ready(function () {
    const tabelaElemento = $('#tabela-consultas');
    // Verifica se há linhas de dados válidas (ignora a linha de mensagem 'empty' se ela existir)
    const possuiDados = tabelaElemento.find('tbody tr').length > 0 && !tabelaElemento.find('tbody tr').hasClass('dataTables_empty');
    
    let tabela;

    if (possuiDados) {
        // Inicializa o DataTables APENAS se houver dados para evitar o erro.
        tabela = tabelaElemento.DataTable({
            dom: 'lrtip',
            paging: false,      // desativa paginação
            info: false,        // remove "Mostrando X de Y"
            searching: false,   // desativa o campo de pesquisa interno
            ordering: false     // mantém a ordenação clicável nas colunas
        });
    } else {
        // Objeto mock para evitar que o restante do código falhe se a tabela estiver vazia
        tabela = {
            rows: () => ({ every: () => {} }),
        };
    }
    
    let debounceTimer;

    function aplicarFiltro() { // Função principal para aplicar todos os filtros
        const filtros = [
            $('#searchInput').val().toLowerCase(),
            $('#tipos').val() ? $('#tipos').val().toLowerCase() : '',
            $('#status').val() ? $('#status').val().toLowerCase() : '',
            $('#data').val() ? $('#data').val().toLowerCase() : ''
        ];

        // Usa o objeto 'tabela' que foi inicializado ou mockado
        tabela.rows().every(function() {
            const rowNode = $(this.node());
            const dataSearch = (rowNode.data('search') || '').toLowerCase();

            // Verifica se TODOS os filtros (não vazios) são encontrados na linha (AND)
            const corresponde = filtros.every(filtro => 
                filtro === '' || dataSearch.includes(filtro)
            );

            // Oculta ou exibe a linha
            rowNode.toggle(corresponde);
        });
    }

    // --- Monitoramento de Filtros ---

    // 1. Aplica o DEBOUNCE ao campo de pesquisa de texto
    $('#searchInput').on('keyup', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(aplicarFiltro, 300);
    });

    // 2. Aplica o filtro IMEDIATAMENTE aos campos de seleção (select/data)
    $('#tipos, #status, #data').on('change', aplicarFiltro);

    // --- Limpar Filtros ---
    $('#clean-filter').on('click', () => {
        // Limpa todos os campos de filtro (sintaxe corrigida)
        $('#searchInput').val('');
        $('#tipos').val('');
        $('#status').val('');
        $('#data').val('');
        
        // Dispara o filtro para reexibir todos os resultados
        aplicarFiltro();
    });
});