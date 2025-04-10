# Desafio Técnico Gntech - API de Dados Climáticos

## 1. Objetivo

Este projeto foi desenvolvido como parte do processo seletivo para a vaga de Desenvolvedor de Sistemas na Gntech. O objetivo é demonstrar habilidades em:

*   Extração de dados de uma API pública (OpenWeatherMap).
*   Armazenamento dos dados em um banco de dados relacional (PostgreSQL).
*   Criação de uma API RESTful (usando FastAPI) para consultar os dados armazenados.
*   Conteinerização da aplicação e do banco de dados usando Docker e Docker Compose.
*   Versionamento de código com Git e organização do projeto no GitHub.

## 2. Tecnologias Utilizadas

*   **Linguagem:** Python 3.9
*   **Framework API:** FastAPI
*   **Banco de Dados:** PostgreSQL 15 (via Docker)
*   **ORM / Driver DB:** SQLAlchemy, psycopg2-binary
*   **Requisições HTTP:** requests
*   **Gerenciamento de Configuração:** python-dotenv, pydantic-settings
*   **Servidor ASGI:** Uvicorn
*   **Conteinerização:** Docker, Docker Compose
*   **Documentação API:** Swagger UI & ReDoc (gerados automaticamente pelo FastAPI)
*   **Versionamento:** Git, GitHub

## 3. Funcionalidades

*   Busca dados climáticos atuais (temperatura, sensação térmica, descrição, umidade, vento) da API OpenWeatherMap para uma cidade especificada.
*   Armazena os dados coletados em uma tabela no banco de dados PostgreSQL.
*   Fornece endpoints RESTful para:
    *   Buscar e salvar dados climáticos de uma cidade (`POST /weather/{city}`).
    *   Listar todos os registros climáticos armazenados (`GET /weather/`).
    *   Listar todos os registros climáticos armazenados para uma cidade específica (`GET /weather/{city}`).
    *   Obter o registro climático mais recente armazenado para uma cidade específica (`GET /weather/latest/{city}`).
*   Ambiente totalmente conteinerizado com Docker, facilitando a execução em qualquer máquina.
*   Documentação interativa da API disponível via Swagger UI e ReDoc.

## 4. Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

*   [Git](https://git-scm.com/)
*   [Docker](https://www.docker.com/products/docker-desktop/)
*   [Docker Compose](https://docs.docker.com/compose/install/) (geralmente incluído no Docker Desktop)
*   Uma **Chave de API (API Key) válida do OpenWeatherMap**. Você pode obter uma gratuitamente em [openweathermap.org/appid](https://openweathermap.org/appid).

## 5. Configuração do Ambiente

Siga estes passos para configurar o projeto localmente:

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/GuilhermeLeandro/gntech-challenge.git
    cd gntech-challenge # Ou o nome que você deu ao diretório
    ```

2.  **Crie o Arquivo de Variáveis de Ambiente (`.env`):**
    *   Copie o arquivo de exemplo:
        ```bash
        cp .env.example .env
        ```
    *   **IMPORTANTE:** O arquivo `.env` contém informações sensíveis e **não deve** ser versionado no Git (ele já está incluído no `.gitignore`).
    *   Abra o arquivo `.env` recém-criado em um editor de texto e preencha as variáveis:

        *   `OPENWEATHER_API_KEY`: Cole aqui a sua chave de API válida do OpenWeatherMap. **A aplicação não funcionará sem uma chave válida.**
        *   `POSTGRES_USER`: Defina o nome de usuário para o banco de dados que será criado dentro do container Docker (ex: `user_db`, `root`).
        *   `POSTGRES_PASSWORD`: Defina uma senha para o usuário do banco de dados Docker.
        *   `POSTGRES_DB`: Defina o nome do banco de dados que será criado dentro do container Docker (ex: `weather_db`).
        *   `DATABASE_URL`: **Verifique se esta linha está correta e descomentada.** Ela usa as variáveis acima para formar a string de conexão que a API (rodando no container `api`) usará para se conectar ao banco (rodando no container `db`). O formato deve ser: `postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}`. **O host `@db` é essencial**, pois `db` é o nome do serviço do banco de dados no `docker-compose.yml`.

## 6. Executando a Aplicação com Docker

Com o Docker e o Docker Compose instalados e o arquivo `.env` configurado:

1.  **Navegue até a Raiz do Projeto:** Certifique-se de que você está no diretório principal (`gntech-challenge/`) onde os arquivos `Dockerfile` e `docker-compose.yml` estão localizados.

2.  **Execute o Docker Compose:**
    ```bash
    docker-compose up --build -d
    ```
    *   `up`: Cria e inicia os containers definidos no `docker-compose.yml`.
    *   `--build`: Força a reconstrução da imagem Docker da API caso haja alterações no código ou no `Dockerfile`. Necessário na primeira execução.
    *   `-d`: Executa os containers em modo "detached" (segundo plano), liberando seu terminal.

3.  **Aguarde:** Na primeira execução, o Docker fará o download da imagem do PostgreSQL e construirá a imagem da API (instalando dependências Python), o que pode levar alguns minutos.

4.  **Verifique os Containers:** Para confirmar que ambos os containers (API e Banco de Dados) estão rodando:
    ```bash
    docker ps
    ```
    Você deve ver dois containers listados (`gntech_fastapi_api` e `gntech_postgres_db` ou nomes similares) com o status "Up".

## 7. Acessando e Usando a API

Após iniciar os containers:

1.  **Documentação Interativa (Swagger UI):**
    *   Abra seu navegador e acesse: `http://localhost:8000/docs`
    *   Esta interface permite visualizar todos os endpoints disponíveis, seus parâmetros, e **executar requisições de teste diretamente do navegador**.

2.  **Documentação Alternativa (ReDoc):**
    *   Acesse: `http://localhost:8000/redoc`
    *   Oferece uma visualização diferente da documentação da API.

3.  **Endpoints Disponíveis (Teste via Swagger):**

    *   **`POST /weather/{city}`**
        *   **Descrição:** Busca os dados climáticos atuais da cidade informada no OpenWeatherMap, salva no banco de dados e retorna o registro criado.
        *   **Parâmetros:** `city` (string, na URL) - Nome da cidade (ex: `Sao Paulo`, `London`).
        *   **Resposta Sucesso:** `201 Created` com o JSON dos dados salvos.
        *   **Como Testar:** Expanda a seção POST, clique em "Try it out", digite o nome da cidade, e clique em "Execute".

    *   **`GET /weather/`**
        *   **Descrição:** Retorna uma lista de todos os registros climáticos armazenados no banco de dados, ordenados pelos mais recentes.
        *   **Parâmetros:** Nenhum.
        *   **Resposta Sucesso:** `200 OK` com uma lista (JSON array) de todos os registros.
        *   **Como Testar:** Expanda a seção GET, clique em "Try it out", e clique em "Execute".

    *   **`GET /weather/{city}`**
        *   **Descrição:** Retorna uma lista de todos os registros climáticos armazenados para a cidade especificada, ordenados pelos mais recentes.
        *   **Parâmetros:** `city` (string, na URL) - Nome da cidade a filtrar.
        *   **Resposta Sucesso:** `200 OK` com uma lista (JSON array) dos registros da cidade.
        *   **Resposta Erro:** `404 Not Found` se nenhum registro for encontrado para a cidade no banco.
        *   **Como Testar:** Expanda a seção GET, clique em "Try it out", digite o nome da cidade, e clique em "Execute".

    *   **`GET /weather/latest/{city}`**
        *   **Descrição:** Retorna o registro climático mais recente armazenado para a cidade especificada.
        *   **Parâmetros:** `city` (string, na URL) - Nome da cidade.
        *   **Resposta Sucesso:** `200 OK` com um único objeto JSON do registro mais recente.
        *   **Resposta Erro:** `404 Not Found` se nenhum registro for encontrado para a cidade no banco.
        *   **Como Testar:** Expanda a seção GET, clique em "Try it out", digite o nome da cidade, e clique em "Execute".

## 8. Estrutura do Banco de Dados

A aplicação utiliza uma única tabela no PostgreSQL chamada `weather_data` para armazenar os dados coletados. Os principais campos são:

*   `id` (Integer, Primary Key): Identificador único do registro.
*   `city` (String): Nome da cidade.
*   `temperature` (Float): Temperatura em graus Celsius.
*   `feels_like` (Float): Sensação térmica em graus Celsius.
*   `description` (String): Descrição do tempo (ex: "céu limpo", "chuva moderada").
*   `humidity` (Integer): Percentual de umidade.
*   `wind_speed` (Float): Velocidade do vento (m/s).
*   `data_timestamp` (DateTime): Timestamp de quando os dados foram coletados da API OpenWeatherMap (em UTC).
*   `fetched_at` (DateTime): Timestamp de quando o registro foi inserido no banco de dados (gerado pelo servidor).

A tabela é criada automaticamente pela aplicação na primeira inicialização, caso não exista, através do SQLAlchemy (`Base.metadata.create_all`).

## 9. Estrutura do Projeto

A estrutura de pastas e arquivos do projeto está organizada da seguinte forma:

*   `gntech-challenge/` (Diretório Raiz)
    *   `.env`: Arquivo com variáveis de ambiente (NÃO VERSIONADO)
    *   `.env.example`: Arquivo de exemplo para variáveis de ambiente
    *   `.gitignore`: Arquivos ignorados pelo Git
    *   `Dockerfile`: Instruções para construir a imagem Docker da API
    *   `docker-compose.yml`: Orquestração dos containers (API + DB)
    *   `requirements.txt`: Dependências Python
    *   `README.md`: Este arquivo de documentação
    *   `app/`: Código fonte da aplicação FastAPI
        *   `__init__.py`
        *   `config.py`: Carregamento de configurações (.env)
        *   `main.py`: Ponto de entrada da aplicação FastAPI
        *   `api/`: Endpoints da API (rotas)
            *   `__init__.py`
            *   `endpoints.py`
        *   `db/`: Módulos relacionados ao banco de dados
            *   `__init__.py`
            *   `database.py`: Configuração da conexão e sessão SQLAlchemy
            *   `models.py`: Modelos ORM (definição da tabela)
            *   `schemas.py`: Schemas Pydantic (validação de dados)
        *   `services/`: Lógica de negócio
            *   `__init__.py`
            *   `weather_service.py`: Busca na API externa e interação com DB


## 10. Parando a Aplicação

Para parar e remover os containers criados pelo Docker Compose:

1.  No terminal, na raiz do projeto, execute:
    ```bash
    docker-compose down
    ```
2.  Este comando para e remove os containers e a rede, mas **NÃO** remove o volume de dados do PostgreSQL (`postgres_data`) por padrão. Isso significa que se você executar `docker-compose up` novamente, os dados anteriores ainda estarão lá.

3.  Se você quiser parar os containers **E remover o volume de dados** (apagando todos os dados do banco de dados Docker), use:
    ```bash
    docker-compose down -v
    ```

---

Obrigado pela oportunidade de participar deste desafio!
