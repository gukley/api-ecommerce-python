# 🧠 GGTECH - Back-end (FastAPI + Docker + PostgreSQL)

Este repositório contém o **back-end do sistema GGTECH**, desenvolvido em **FastAPI**.  
O sistema foi configurado e adaptado por mim a partir de uma base existente, com diversas melhorias e novas implementações voltadas ao **gerenciamento de usuários, produtos, pedidos e integração com pagamentos via Stripe**.

O objetivo principal deste back-end é fornecer uma **API robusta, escalável e segura** para o e-commerce GGTECH, que compõe o projeto de **Trabalho de Conclusão de Curso (TCC)**.

---

## 📦 Tecnologias Utilizadas

- **FastAPI** — Framework moderno e performático para APIs em Python  
- **PostgreSQL** — Banco de dados relacional  
- **Docker e Docker Compose** — Containerização da aplicação e do banco de dados  
- **Uvicorn** — Servidor ASGI leve e rápido  
- **Stripe API** — Integração para pagamentos online  
- **Pydantic & SQLAlchemy** — Modelagem e validação de dados  
- **Dev Containers (VSCode)** — Ambiente de desenvolvimento isolado e reprodutível  

---

## ⚙️ Requisitos do Ambiente

- **Docker** instalado na máquina  
- **VS Code** (recomendado para uso com contêineres)  
- Extensão **[Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)** instalada  

> Esses recursos garantem um ambiente padronizado e evitam erros de configuração entre máquinas.

---

## 🔐 Configuração do Arquivo `.env`

Antes de iniciar o projeto, crie um arquivo chamado `.env` na raiz do repositório e copie o conteúdo do arquivo `.env.example` para ele.

O arquivo `.env` contém variáveis de ambiente essenciais, como:

```env
DATABASE_URL=postgresql://user:password@db:5432/ggtech
STRIPE_SECRET_KEY=chave_secreta_stripe
JWT_SECRET=chave_jwt


🚀 Execução com Docker (Recomendado)

Este é o método ideal de execução, pois não exige a instalação local do Python ou PostgreSQL — todo o ambiente é configurado automaticamente via contêineres Docker.

Passos:

1. Instale o Docker Desktop

2. Abra o projeto no VS Code

3. Certifique-se de que a extensão Dev Containers está instalada

4. Pressione F1 (ou Ctrl+Shift+P) e selecione:
“Dev Containers: Reopen in Container” ou “Rebuild and Reopen in Container”

5. O VS Code irá:

. Ler o arquivo docker-compose.yml
. Subir os contêineres:
   .app → aplicação FastAPI
   .db → banco de dados PostgreSQL
. Instalar automaticamente as dependências via requirements.txt

Após a configuração:

. API disponível em: http://localhost:8000
. Documentação Swagger: http://localhost:8000/docs

💻 Execução Local (sem Docker)

Também é possível rodar o projeto localmente, caso prefira não utilizar contêineres.

Passos:

1. Instale o Python 3.9+
2. Crie e ative um ambiente virtual:

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

3. Instale as dependências:
pip install -r requirements.txt

4. Execute a aplicação:
uvicorn main:app --reload

5. Acesse:
. API: http://localhost:8000
. Documentação Swagger: http://localhost:8000/docs

⚠️ Nesse modo, o banco de dados não é criado automaticamente.
Caso queira usar PostgreSQL localmente, configure a variável DATABASE_URL no .env.

🧩 Estrutura do Projeto

📦 ggtech-backend
 ┣ 📂 app
 ┃ ┣ 📂 api          → Rotas e controladores da aplicação
 ┃ ┣ 📂 controllers  → Lógica de recursos (usuários, produtos, pedidos, etc.)
 ┃ ┣ 📂 core         → Configurações principais (autenticação, CORS, etc.)
 ┃ ┣ 📂 models       → Modelos de dados (SQLAlchemy)
 ┃ ┣ 📂 schemas      → Validações e DTOs (Pydantic)
 ┃ ┣ 📂 services     → Regras de negócio e integrações (ex: Stripe)
 ┃ ┗ 📜 main.py      → Ponto de entrada da aplicação FastAPI
 ┣ 📂 alembic        → Migrações do banco de dados
 ┣ 📂 uploads        → Armazenamento de imagens (produtos, categorias, perfis)
 ┣ 📂 db             → Diagramas e scripts de modelagem do banco
 ┣ 📜 docker-compose.yml  → Configuração dos contêineres Docker
 ┣ 📜 requirements.txt     → Dependências do projeto
 ┣ 📜 .env.example         → Exemplo de variáveis de ambiente
 ┗ 📜 README.md            → Documentação do projeto

🧠 Observações

. Este projeto foi originalmente baseado em um repositório público, mas recebeu diversas adaptações e melhorias:
. Implementação de novas rotas e endpoints
. Integração completa com Stripe
. Ajustes de segurança e autenticação JWT
. Refatorações para melhor desempenho e legibilidade do código
. Todo o ambiente é containerizado, o que facilita o deploy e a execução em qualquer máquina.


