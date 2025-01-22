# Meu Projeto FastAPI

Este projeto é um exemplo de aplicação **FastAPI** que utiliza **PostgreSQL** como banco de dados e se integra perfeitamente ao **Docker** e ao **VS Code Dev Containers** para desenvolvimento.

## Sumário

1. [Requisitos](#requisitos)  
2. [Criando o arquivo `.env`](#criando-o-arquivo-env)  
3. [Executando com Docker e Dev Containers (Recomendado)](#executando-com-docker-e-dev-containers-recomendado)  
4. [Executando localmente sem Docker (sem banco)](#executando-localmente-sem-docker-sem-banco)  
5. [Estrutura de Pastas (Visão Geral)](#estrutura-de-pastas-visão-geral)  
6. [Endpoints](#endpoints)

---

## Requisitos

- **Docker** instalado na máquina.  
- **VS Code** (opcional, mas fortemente recomendado se quiser usar Dev Containers).  
- **Extensão “[Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)”** (ou “Remote - Containers”) instalada no VS Code (caso use o fluxo de Dev Containers).

---

## Criando o arquivo `.env`

Antes de subir o projeto, crie um arquivo chamado `.env` na raiz do projeto e copie o conteúdo do outro arquivo `.env.example` para ele.

---

## Executando com Docker e Dev Containers (Recomendado)

Este é o cenário principal, que **não** exige ter Python instalado localmente, pois todo o ambiente de desenvolvimento (Python, dependências, banco de dados) roda no Docker.

1. **Instale o Docker** (Docker Engine ou Docker Desktop, dependendo do seu sistema operacional).
2. **Instale o VS Code** e abra-o.
3. **Instale a extensão** “[Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)” (também conhecida como “Remote - Containers”).
4. **Abra o projeto no VS Code**.
5. Pressione **F1** (ou `Ctrl+Shift+P`) e procure por **“Dev Containers: Reopen in Container”** (ou “Rebuild and Reopen in Container”).
6. O VS Code irá:
   - Ler o arquivo `docker-compose.yml` e subir os contêineres:
     - `app` (sua aplicação FastAPI)
     - `db` (PostgreSQL)
   - Acessar o contêiner onde está o Python e instalar extensões (Python, Pylance, etc.) definidas em `.devcontainer/devcontainer.json`.
   - Executar `pip install -r requirements.txt`.

Quando terminar, você estará em um ambiente de desenvolvimento isolado dentro do contêiner Docker.

- A aplicação poderá ser acessada em **http://localhost:8000**.  
- Para testar a API, vá em **http://localhost:8000/docs**.

---

## Executando localmente sem Docker (sem banco)

Se você **não** quiser usar Docker e preferir rodar localmente, então:

1. **Instale Python 3.9+** localmente.
2. **Crie um virtual environment** (recomendado) e ative-o:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```
3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Inicie a aplicação**:
   ```bash
   uvicorn main:app --reload
   ```
5. Acesse **http://localhost:8000** e **http://localhost:8000/docs**.

> **Importante**: Nesse modo local sem Docker, o banco de dados **não** está configurado. Você pode adicionar manualmente um Postgres local e ajustar o `DATABASE_URL`, mas isso exigiria configurações adicionais. Caso queira um banco local, você precisará instalá-lo no sistema ou configurar de outra forma.

---
