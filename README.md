# 🦷 Tooth & Care - Sistema de Gestão de Clínica Odontológica

![Badge - Status do Projeto](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![Badge - Linguagem Principal](https://img.shields.io/badge/Feito%20com-Python-blue)
![Badge - Framework](https://img.shields.io/badge/Framework-Django-092E20)
![Badge - Licença](https://img.shields.io/badge/Licença-MIT-green)

---

## 💡 Sobre o Projeto

O **Tooth & Care** é um sistema web desenvolvido como projeto final do curso técnico de Análise e Desenvolvimento de Sistemas do SENAI. O objetivo principal é simular e gerenciar digitalmente uma clínica odontológica completa. O sistema visa **digitalizar e agilizar o processo de consultas**, desde o agendamento pelo paciente até a emissão de diagnósticos pelo dentista, proporcionando agilidade e organização para toda a equipe.

### 🎯 Público-Alvo

O sistema foi arquitetado para atender a três perfis de usuários, cada um com acesso a funcionalidades específicas:

1.  **Pacientes (Clientes):** Para agendamento e acompanhamento de consultas.
2.  **Médicos (Dentistas):** Para realização de consultas e emissão de diagnósticos.
3.  **Administradores:** Para gerenciamento geral da clínica, médicos e pacientes.

## 🌟 Funcionalidades Principais

| Perfil de Usuário | Funcionalidades Chave |
| :--- | :--- |
| **Paciente** | Criação e gestão de conta, **Agendamento** online de consultas, Histórico de agendamentos. |
| **Médico** | Visualização da agenda diária, **Realização de Consultas**, Criação e edição de **Prontuários e Diagnósticos**. |
| **Administrador** | Gerenciamento completo de **Contas de Médicos e Pacientes**, Controle geral do fluxo de agendamentos. |

## ⚙️ Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando uma arquitetura robusta baseada nas seguintes tecnologias:

* **Linguagem Principal:** Python 
* **Framework Web:** Django
* **Banco de Dados:** SQLite (padrão Django para desenvolvimento)
* **Front-end:** HTML, CSS, JavaScript

## 🚀 Configuração e Instalação

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Pré-requisitos
Certifique-se de ter o **Python 3.x** e o **pip** instalados.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/SENAI-Morvan-Figueiredo/Clinica-tooth-and-care](https://github.com/SENAI-Morvan-Figueiredo/Clinica-tooth-and-care)
cd Clinica-tooth-and-care
```

### 2. Criar e Ativar o Ambiente Virtual
Recomendamos o uso de ambientes virtuais para isolar as dependências do projeto.

```Bash
# Cria o ambiente virtual
python -m venv venv 

# Ativa o ambiente virtual (Windows)
.\venv\Scripts\activate 

# Ativa o ambiente virtual (Linux/macOS)
source venv/bin/activate 
```

### 3. Instalar as Dependências
Instale todas as bibliotecas Python necessárias.

```Bash
pip install -r requirements.txt
```

### 4. Aplicar as Migrações
Crie o banco de dados e as tabelas necessárias.

```Bash
python manage.py migrate
```

### 5. Criar o Superusuário (Administrador)
Crie uma conta de administrador para acessar o painel de gerenciamento do Django.

```Bash
python manage.py createsuperuser
```

### 6. Executar o Servidor
Inicie o servidor de desenvolvimento local.

```Bash
python manage.py runserver
```

O sistema estará disponível em: http://127.0.0.1:8000/