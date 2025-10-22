document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('.paciente-checkbox');
    const allcheckbox = document.getElementById('select-all');

    allcheckbox.addEventListener('change', (e) => { 
        checkboxes.forEach(cb => cb.checked = e.target.checked);
    });

    function checkAll() {
        let all = true;
        checkboxes.forEach(cb => {
            if(!cb.checked) all = false;
        });
        
        if(all) {
            allcheckbox.checked = true;
        } else {
            allcheckbox.checked = false;
        }
    }

    checkboxes.forEach(cb => {
        cb.addEventListener('change', (e) => {
            checkAll();
        });
    });
});

$(document).ready(function() {
    const tabela = $('#tabela-pacientes').DataTable({
        dom: 'lrtip',
        paging: false, // desativa paginação
        info: false,   // remove "Mostrando X de Y"
        searching: false, // desativa o campo de pesquisa interno
        ordering: false    // mantém a ordenação clicável nas colunas
    });

// filtra para cada tecla apertada
    document.getElementById('searchInput').addEventListener('keyup', function() {
        tabela.rows().every(function() {
            const termo = $('#searchInput').val().toLowerCase();
            const dataSearch = $(this.node()).data('search') || '';
            const corresponde = dataSearch.toLowerCase().includes(termo);
            $(this.node()).toggle(corresponde);
        });
    });
});