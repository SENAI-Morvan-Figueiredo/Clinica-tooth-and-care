document.addEventListener('DOMContentLoaded', function () {
    // Seletores do formulário
    const servicoSelect = document.getElementById('id_servico');
    const medicoSelect = document.getElementById('id_medico');
    const dataWrapper = document.getElementById('id_data_wrapper');
    const horaSelect = document.getElementById('id_hora_consulta');
    const salaInput = document.getElementById('id_sala');

    let datasDisponiveis = [];

    if (!servicoSelect || !medicoSelect || !dataWrapper || !horaSelect || !salaInput) {
        console.error("Um ou mais campos do formulário de agendamento não foram encontrados. Verifique os IDs.");
        return;
    }

    // Inicialmente desabilitar médico, data e hora
    medicoSelect.disabled = true;
    dataWrapper.querySelectorAll('select').forEach(select => {
        select.disabled = true;
    });
    horaSelect.disabled = true;

    /**
     * Função que busca os médicos disponíveis para o serviço selecionado
     */
    function updateMedicos() {
        const servico = servicoSelect.value;
        const urlAPI = '/api/carrega_medicos/';

        // Limpa e desabilita campos dependentes
        medicoSelect.innerHTML = '<option value="">Selecione um médico</option>';
        medicoSelect.disabled = true;

        dataWrapper.querySelectorAll('select').forEach(select => {
            select.value = '';
            select.disabled = true;
        });

        horaSelect.innerHTML = '<option value="">Selecione o médico e a data</option>';
        horaSelect.disabled = true;
        salaInput.value = '';

        if (!servico) {
            return;
        }

        // Faz a requisição Fetch para a API
        fetch(`${urlAPI}?servico=${servico}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro de rede ou servidor: ${response}`);
                }
                return response.json();
            })
            .then(data => {
                // Limpa e habilita o campo de médico
                medicoSelect.innerHTML = '<option value="">--- Escolha o Médico ---</option>';
                medicoSelect.disabled = false;


                if (data && data.length > 0) {
                    // Preenche o Select de Médicos
                    data.forEach(medico => {
                        const option = document.createElement('option');
                        option.value = medico.id;
                        option.textContent = medico.user__first_name + ' ' + medico.user__last_name;
                        medicoSelect.appendChild(option);
                    });
                } else {
                    medicoSelect.innerHTML = '<option value="" disabled>Nenhum médico disponível para este serviço</option>';
                }
            })
            .catch(error => {
                console.error("Erro ao buscar médicos:", error);
                medicoSelect.innerHTML = '<option value="">Erro ao carregar médicos.</option>';
                medicoSelect.disabled = true;
            });
    }

    /**
     * Função que habilita o campo de data quando um médico é selecionado
     */
    function enableDataField() {
        const medicoId = medicoSelect.value;

        dataWrapper.querySelectorAll('select').forEach(select => {
            select.disabled = !medicoId;
            if (!medicoId) {
                select.value = '';
            }
        });

        if (!medicoId) {
            horaSelect.innerHTML = '<option value="">Selecione o médico e a data</option>';
            horaSelect.disabled = true;
            salaInput.value = '';
        } else {
            // Se temos um médico selecionado, buscar as datas disponíveis
            updateDatasDisponiveis();
        }
    }

    /**
     * Função que busca as datas disponíveis para o médico selecionado
     */
    function updateDatasDisponiveis() {
        const medicoId = medicoSelect.value;
        const urlAPI = '/api/carrega_datas/';

        if (!medicoId) {
            return;
        }

        // Limpa a variável de datas disponíveis
        datasDisponiveis = [];

        // Desabilita e limpa a seleção de hora
        horaSelect.innerHTML = '<option value="">Selecione uma data primeiro</option>';
        horaSelect.disabled = true;
        salaInput.value = '';

        // Faz a requisição Fetch para a API de datas disponíveis
        fetch(`${urlAPI}?medico_id=${medicoId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro de rede ou servidor: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                datasDisponiveis = data || [];

                // Habilita os selects de data
                dataWrapper.querySelectorAll('select').forEach(select => {
                    select.disabled = false;
                });

            })
            .catch(error => {
                console.error("Erro ao buscar datas disponíveis:", error);
                datasDisponiveis = [];
            });
    }


    /**
     * Função que busca os horários disponíveis via AJAX
     */
    function updateHorarios() {
        const medicoId = medicoSelect.value;
        const ano = document.getElementById('id_data_0').value;
        const mes = document.getElementById('id_data_1').value;
        const dia = document.getElementById('id_data_2').value;
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
                salaInput.value = '';

                if (data.slots && data.slots.length > 0) {
                    // Preenche o Select de Horas
                    data.slots.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot.hora;
                        option.textContent = slot.hora;
                        option.dataset.sala = slot.sala;
                        horaSelect.appendChild(option);
                    });

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
     * Função que atualiza o campo Sala com base na Hora selecionada
     */
    function updateSala() {
        const selectedOption = horaSelect.options[horaSelect.selectedIndex];
        const sala = selectedOption ? selectedOption.dataset.sala : '';
        salaInput.value = sala || '';
    }

    // --- Configuração dos Event Listeners ---
    servicoSelect.addEventListener('change', updateMedicos);
    medicoSelect.addEventListener('change', enableDataField);

    // Adicionar um Event Listener em cada select (dia, mês, ano)
    dataWrapper.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', updateHorarios);
    });

    horaSelect.addEventListener('change', updateSala);

    // Se o formulário for carregado com dados (edição), atualizar os campos
    if (servicoSelect.value) {
        updateMedicos();
    }
    if (medicoSelect.value) {
        enableDataField();
    }
});