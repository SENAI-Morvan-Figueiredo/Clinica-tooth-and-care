$(document).ready(function() {
    const tabela = $('#medicosTable').DataTable({
        dom: 'lrtip',
        paging: false, // desativa paginação
        info: false,   // remove "Mostrando X de Y"
        searching: false, // desativa o campo de pesquisa interno
        ordering: false    // mantém a ordenação clicável nas colunas
    });

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