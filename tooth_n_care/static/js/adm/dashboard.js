$(document).ready(function() {
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

    // função filtro
    function filtrar() {
        const filtros = [
            $('#searchInput').val().toLowerCase(),
            $('#especialidade').val() ? $('#especialidade').val().toLowerCase() : ''
        ];

        tabela.rows().every(function() {
            const dataSearch = ($(this.node()).data('search') || '').toLowerCase();

            // Verifica se todos os filtros correspondem com o dado
            const corresponde = filtros.every(filtro => {
                return filtro === '' || dataSearch.includes(filtro);
            });
            
            $(this.node()).toggle(corresponde);
        });
    }

    //event listeners
    $('#searchInput, #especialidade').on('keyup change', filtrar);
});