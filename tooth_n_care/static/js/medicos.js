document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('.medico-checkbox');
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