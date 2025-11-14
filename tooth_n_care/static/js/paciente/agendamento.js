document.addEventListener('DOMContentLoaded', function() {
    // Seletores do formulário
    const medicoSelect = document.getElementById('id_medico');
    // Renomear o seletor para capturar a mudança em qualquer um dos selects do SelectDateWidget
    const dataWrapper = document.getElementById('id_data_wrapper'); 
    const horaSelect = document.getElementById('id_hora_consulta');
    const salaInput = document.getElementById('id_sala');

    if (!medicoSelect || !dataWrapper || !horaSelect || !salaInput) {
        console.error("Um ou mais campos do formulário de agendamento não foram encontrados. Verifique os IDs.");
        return;
    }

    /**
     * Função que busca os horários disponíveis via AJAX e atualiza os campos Hora e Sala.
     */
    function updateHorarios() {
        const medicoId = medicoSelect.value;
        const ano = document.getElementById('id_data_0').value; // id_data_0 para ano
        const mes = document.getElementById('id_data_1').value; // id_data_1 para mês
        const dia = document.getElementById('id_data_2').value; // id_data_2 para dia
        const dataSelecionada = `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`;
        const urlAPI = '/consultas/api/disponibilidade/'; 

        // Desabilita e limpa a seleção de hora se o Médico ou a Data não estiverem selecionados
        if (!medicoId || !ano || !mes || !dia) {
            horaSelect.innerHTML = '<option value="">Selecione o Médico e a Data</option>';
            horaSelect.disabled = true;
            salaInput.value = '';
            return;
        }

        // Faz a requisição Fetch para a API
        fetch(`${urlAPI}?medico_id=${medicoId}&data=${dataSelecionada}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro de rede ou servidor: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Limpa e habilita o campo de hora
                horaSelect.innerHTML = '<option value="">--- Escolha a Hora ---</option>';
                horaSelect.disabled = false;
                salaInput.value = ''; // Limpa a sala

                if (data.slots && data.slots.length > 0) {
                    // Preenche o Select de Horas
                    data.slots.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot.hora;
                        option.textContent = slot.hora;
                        // Armazena a sala no atributo de dados
                        option.dataset.sala = slot.sala; 
                        horaSelect.appendChild(option);
                    });
                    
                    // Define o valor da sala como a sala do primeiro slot disponível por padrão (se nenhum estiver selecionado)
                    // Ou mantém o valor anterior se o usuário já tiver selecionado um
                    if (!horaSelect.value) {
                        salaInput.value = data.slots[0].sala;
                    }
                    
                } else {
                    horaSelect.innerHTML = '<option value="" disabled>Nenhum horário disponível</option>';
                    salaInput.value = '';
                }
            })
            .catch(error => {
                console.error("Erro ao buscar disponibilidade:", error);
                horaSelect.innerHTML = '<option value="">Erro ao carregar horários.</option>';
                horaSelect.disabled = true;
                salaInput.value = '';
            });
    }
    
    /**
     * Função que atualiza o campo Sala com base na Hora selecionada.
     */
    function updateSala() {
        const selectedOption = horaSelect.options[horaSelect.selectedIndex];
        // Pega o valor do atributo data-sala do <option> selecionado
        const sala = selectedOption ? selectedOption.dataset.sala : '';
        salaInput.value = sala || ''; // Define o valor da sala no campo oculto/readonly
    }

    // --- Configuração dos Event Listeners ---
    medicoSelect.addEventListener('change', updateHorarios);
    
    // Adicionar um Event Listener em cada select (dia, mês, ano)
    dataWrapper.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', updateHorarios);
    });

    horaSelect.addEventListener('change', updateSala); // Atualiza a sala sempre que a hora muda

    // Chamada inicial para preencher se o formulário for carregado com dados (ex: edição)
    updateHorarios();
});