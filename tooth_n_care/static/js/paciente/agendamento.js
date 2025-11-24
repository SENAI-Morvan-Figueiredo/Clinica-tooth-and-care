document.addEventListener('DOMContentLoaded', function () {
    // cancelamento de consultas
    document.querySelectorAll('.cancel-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const dialog = document.getElementById(btn.dataset.dialogId);
            if (dialog && typeof dialog.showModal === 'function') {
                dialog.showModal(); // Use showModal para o backdrop
            } else if (dialog) {
                dialog.show();
            }
        });
    });

    document.querySelectorAll('.close-dialog-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const dialog = document.getElementById(btn.dataset.dialogId);
            if (dialog && typeof dialog.close === 'function') {
                dialog.close(); 
            }
        });
    });

    // Seletores do formulário
    const servicoSelect = document.getElementById('id_servico');
    const medicoSelect = document.getElementById('id_medico');
    const dataSelect = document.getElementById("id_data");
    const horaSelect = document.getElementById('id_hora_consulta');
    const salaInput = document.getElementById('id_sala');

    let datasDisponiveis = [];

    if (!servicoSelect || !medicoSelect || !dataSelect || !horaSelect || !salaInput) {
        console.error("Um ou mais campos do formulário de agendamento não foram encontrados. Verifique os IDs.");
        return;
    }

    // Inicialmente desabilitar médico, data e hora
    medicoSelect.disabled = true;
    dataSelect.disabled = true;
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

        dataSelect.innerHTML = 
        dataSelect.disabled = true;

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

        dataSelect.disabled = !medicoId;
        if (!medicoId) {
            dataSelect.innerHTML = '<option value=\"">Selecione um médico</option>';
        }

        if (!medicoId) {
            horaSelect.innerHTML = '<option value=\"">Selecione o médico e a data</option>';
            horaSelect.disabled = true;
            salaInput.value = "";
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
        const urlAPI = "/api/carrega_datas/";

        if (!medicoId) {
            return;
        }

        // Limpa a variável de datas disponíveis
        datasDisponiveis = [];

        // Desabilita e limpa a seleção de hora
        horaSelect.innerHTML = '<option value=\"">Selecione uma data primeiro</option>';
        horaSelect.disabled = true;
        salaInput.value = "";

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
                dataSelect.innerHTML = '<option value=\"">--- Escolha a Data ---</option>';

                if (datasDisponiveis.length > 0) {
                    datasDisponiveis.forEach(data => {
                        const option = document.createElement("option");
                        option.value = data;
                        option.textContent = new Date(data + "T00:00:00").toLocaleDateString("pt-BR");
                        dataSelect.appendChild(option);
                    });
                    dataSelect.disabled = false;
                } else {
                    dataSelect.innerHTML = "<option value=\"\" disabled>Nenhuma data disponível</option>";
                    dataSelect.disabled = true;
                }
            })
            .catch(error => {
                console.error("Erro ao buscar datas disponíveis:", error);
                datasDisponiveis = [];
                dataSelect.innerHTML = "<option value=\"\">Erro ao carregar datas.</option>";
                dataSelect.disabled = true;
            });
    }


    /**
     * Função que busca os horários disponíveis via AJAX
     */
    function updateHorarios() {
        const medicoId = medicoSelect.value;
        const dataSelecionada = dataSelect.value;
        const urlAPI = "/consulta/api/disponibilidade/";

        // Desabilita e limpa a seleção de hora se o Médico ou a Data não estiverem selecionados
        if (!medicoId || !dataSelecionada) {
            horaSelect.innerHTML = '<option value=\"">Selecione o Médico e a Data</option>';
            horaSelect.disabled = true;
            salaInput.value = "";
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

    dataSelect.addEventListener("change", updateHorarios);

    horaSelect.addEventListener('change', updateSala);

    // Se o formulário for carregado com dados (edição), atualizar os campos
    if (servicoSelect.value) {
        updateMedicos();
    }
    if (medicoSelect.value) {
        enableDataField();
    }

    // evita o envio com campos desabilitados
    document.getElementById('agendamento-form').addEventListener('submit', (e) => {
        servicoSelect.disabled = false;
        medicoSelect.disabled = false;
        dataSelect.disabled = false;
        horaSelect.disabled = false;
        salaInput.disabled = false;
    });
});