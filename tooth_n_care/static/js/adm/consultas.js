$(document).ready(function () {
    const tabela = $('#tabela-consultas').DataTable({
        dom: 'lrtip',
        paging: false, // desativa paginação
        info: false,   // remove "Mostrando X de Y"
        searching: false, // desativa o campo de pesquisa interno
        ordering: false    // mantém a ordenação clicável nas colunas
    });

    function filtrar() { // filtra todos os elementos de uma vez
        const filtros = [
            $('#searchInput').val().toLowerCase() ,
            $('#tipos').val() ? $('#tipos').val().toLowerCase() : '',
            $('#status').val() ? $('#status').val().toLowerCase() : '',
            $('#data').val() ? $('#data').val().toLowerCase() : ''
        ];

        tabela.rows().every(function() {
            const dataSearch = ($(this.node()).data('search') || '').toLowerCase();

            // Verifica se todos os filtros são encontrados na linha (AND)
            const corresponde = filtros.every(filtro => 
                filtro === '' || dataSearch.includes(filtro)
            );

            $(this.node()).toggle(corresponde);
        });
    }

    // detecta alterações no filtro
    $('#searchInput, #tipos, #status, #data').on('keyup change', filtrar);

    $('#clean-filter').on('click', () => {
        $('#searchInput').val('');
        $('#tipos').val('');
        $('#status').val('');
        $('#data').val('');
        filtrar();
    });
});





