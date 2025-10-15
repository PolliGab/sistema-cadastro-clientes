# 🚀 Sistema de Cadastro de Clientes - API REST

API REST desenvolvida em Python com FastAPI para gerenciamento de cadastro de clientes, aplicando boas práticas de engenharia de software.

## 📋 Índice

- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
- [Documentação da API](#-documentação-da-api)
- [Testes](#-testes)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Validação e Testes de Integração](#-validação-e-testes-de-integração)
- [Soft Skills: Lidando com Mudanças de Requisitos](#-soft-skills-lidando-com-mudanças-de-requisitos)

## 🛠 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para interação com banco de dados
- **PostgreSQL**: Banco de dados relacional
- **Pydantic**: Validação de dados e serialização
- **Docker & Docker Compose**: Containerização
- **Pytest**: Framework de testes

## 🏗 Arquitetura

O projeto segue uma arquitetura em camadas com separação de responsabilidades:

```
├── models/          # Modelos de dados (SQLAlchemy)
├── schemas/         # Schemas de validação (Pydantic)
├── services/        # Lógica de negócio
├── database/        # Configuração do banco de dados
└── tests/           # Testes unitários e de integração
```

**Princípios aplicados:**
- **Separation of Concerns**: Cada camada tem responsabilidade única
- **Dependency Injection**: Uso de FastAPI Depends
- **Clean Code**: Código legível e bem documentado
- **SOLID**: Princípios de design orientado a objetos

## 📦 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+ (para desenvolvimento local sem Docker)
- Git

## 🚀 Instalação e Execução

### Opção 1: Usando Docker (Recomendado)

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd sistema-cadastro-clientes
```

2. **Inicie os containers:**
```bash
docker-compose up -d
```

3. **Acesse a API:**
- API: http://localhost:8000
- Documentação interativa (Swagger): http://localhost:8000/docs
- Documentação alternativa (ReDoc): http://localhost:8000/redoc

### Opção 2: Execução Local

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd sistema-cadastro-clientes
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Inicie o PostgreSQL com Docker:**
```bash
docker-compose up -d postgres
```

5. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

6. **Execute a aplicação:**
```bash
python main.py
```

## 📚 Documentação da API

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
**GET /** - Verifica se a API está online

**Resposta (200):**
```json
{
  "message": "Sistema de Cadastro de Clientes - API Online",
  "version": "1.0.0"
}
```

---

#### 2. Criar Cliente
**POST /clientes** - Cadastra um novo cliente

**Request Body:**
```json
{
  "nome": "João da Silva",
  "email": "joao.silva@email.com",
  "telefone": "(41) 99999-9999"
}
```

**Resposta (201):**
```json
{
  "id": 1,
  "nome": "João da Silva",
  "email": "joao.silva@email.com",
  "telefone": "(41) 99999-9999",
  "criado_em": "2025-10-13T10:30:00",
  "atualizado_em": null
}
```

**Validações:**
- `nome`: obrigatório, não pode ser vazio
- `email`: obrigatório, deve ser válido, único no sistema
- `telefone`: opcional

**Erros Possíveis:**
- `400`: Email já cadastrado ou validação falhou
- `422`: Dados inválidos (ex: email mal formatado)

---

#### 3. Listar Todos os Clientes
**GET /clientes** - Lista todos os clientes cadastrados

**Resposta (200):**
```json
[
  {
    "id": 1,
    "nome": "João da Silva",
    "email": "joao.silva@email.com",
    "telefone": "(41) 99999-9999",
    "criado_em": "2025-10-13T10:30:00",
    "atualizado_em": null
  },
  {
    "id": 2,
    "nome": "Maria Santos",
    "email": "maria.santos@email.com",
    "telefone": null,
    "criado_em": "2025-10-13T11:00:00",
    "atualizado_em": null
  }
]
```

---

#### 4. Consultar Cliente por ID
**GET /clientes/{id}** - Busca um cliente específico

**Parâmetros:**
- `id` (path): ID do cliente

**Resposta (200):**
```json
{
  "id": 1,
  "nome": "João da Silva",
  "email": "joao.silva@email.com",
  "telefone": "(41) 99999-9999",
  "criado_em": "2025-10-13T10:30:00",
  "atualizado_em": null
}
```

**Erros Possíveis:**
- `404`: Cliente não encontrado

---

#### 5. Buscar Cliente por Nome (Desafio Extra)
**GET /clientes?nome={valor}** - Busca clientes por nome (busca parcial)

**Parâmetros:**
- `nome` (query): Parte do nome a ser buscada

**Exemplo:**
```
GET /clientes?nome=Silva
```

**Resposta (200):**
```json
[
  {
    "id": 1,
    "nome": "João da Silva",
    "email": "joao.silva@email.com",
    "telefone": "(41) 99999-9999",
    "criado_em": "2025-10-13T10:30:00",
    "atualizado_em": null
  },
  {
    "id": 3,
    "nome": "Maria Silva",
    "email": "maria.silva@email.com",
    "telefone": null,
    "criado_em": "2025-10-13T12:00:00",
    "atualizado_em": null
  }
]
```

**Características:**
- Busca case-insensitive
- Busca parcial (encontra "Silva" em "João da Silva")
- Retorna lista vazia se nenhum cliente corresponder

---

### Exemplos de Uso com cURL

**Criar cliente:**
```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João da Silva",
    "email": "joao@email.com",
    "telefone": "41999999999"
  }'
```

**Listar todos:**
```bash
curl GET http://localhost:8000/clientes
```

**Buscar por ID:**
```bash
curl GET http://localhost:8000/clientes/1
```

**Buscar por nome:**
```bash
curl GET http://localhost:8000/clientes?nome=Silva
```

## 🧪 Testes

O projeto possui cobertura completa de testes unitários e de integração.

### Executar Todos os Testes

```bash
pytest
```

### Executar com Cobertura

```bash
pytest --cov=. --cov-report=html
```

O relatório HTML será gerado em `htmlcov/index.html`

### Executar Testes Específicos

```bash
# Apenas testes de service
pytest tests/test_cliente_service.py

# Apenas testes de API
pytest tests/test_api.py

# Teste específico
pytest tests/test_cliente_service.py::TestClienteServiceCriacao::test_criar_cliente_valido
```

### Estrutura de Testes

**tests/test_cliente_service.py** - Testes unitários da camada de serviço:
- ✅ Criação de cliente válido
- ✅ Validação de campos obrigatórios
- ✅ Validação de email duplicado
- ✅ Normalização de dados
- ✅ Busca por ID
- ✅ Busca por nome (completo e parcial)
- ✅ Busca case-insensitive

**tests/test_api.py** - Testes de integração da API:
- ✅ Todos os endpoints (POST, GET, GET by ID)
- ✅ Validação de request/response
- ✅ Códigos de status HTTP
- ✅ Tratamento de erros
- ✅ Busca por nome via query parameter

## 📂 Estrutura do Projeto

```
sistema-cadastro-clientes/
│
├── main.py                      # Ponto de entrada da aplicação
├── requirements.txt             # Dependências Python
├── Dockerfile                   # Imagem Docker da API
├── docker-compose.yml           # Orquestração dos containers
├── pytest.ini                   # Configuração do Pytest
├── .env.example                 # Exemplo de variáveis de ambiente
├── .gitignore                   # Arquivos ignorados pelo Git
│
├── database/
│   └── connection.py            # Configuração SQLAlchemy e PostgreSQL
│
├── models/
│   └── cliente.py               # Model Cliente (SQLAlchemy)
│
├── schemas/
│   └── cliente_schema.py        # Schemas Pydantic (validação)
│
├── services/
│   └── cliente_service.py       # Lógica de negócio
│
└── tests/
    ├── test_cliente_service.py  # Testes unitários
    └── test_api.py              # Testes de integração
```

## ✅ Validação e Testes de Integração

### Como Validar se a API Está Funcionando Corretamente

#### 1. Testes Automatizados

**Testes Unitários:**
- Validam a lógica de negócio isoladamente
- Usam banco de dados em memória (SQLite)
- Executam rapidamente
- Garantem que regras de validação funcionam

**Testes de Integração:**
- Testam os endpoints da API
- Verificam request/response completos
- Validam códigos de status HTTP
- Garantem que a API funciona end-to-end

```bash
python -m pytest
```

#### 2. Testes Manuais

**a) Verificar Health Check:**
```bash
curl http://localhost:8000/
```

**b) Testar Criação de Cliente:**
```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste",
    "email": "teste@email.com"
  }'
```

**c) Verificar Listagem:**
```bash
curl http://localhost:8000/clientes
```

**d) Testar Validações:**
```bash
# Deve falhar - email duplicado
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste 2",
    "email": "teste@email.com"
  }'

# Deve falhar - email inválido
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste",
    "email": "email_invalido"
  }'
```

#### 3. Testes de Integração com o Banco

**a) Verificar Conexão com PostgreSQL:**
```bash
docker-compose ps  # Verificar se containers estão rodando
docker-compose logs postgres  # Ver logs do PostgreSQL
```

**b) Conectar diretamente ao banco:**
```bash
docker exec -it clientes_db psql -U postgres -d clientes_db

# Dentro do psql:
\dt                        # Listar tabelas
SELECT * FROM clientes;    # Verificar dados
\q                         # Sair
```

**c) Testar Persistência:**
```bash
# 1. Criar cliente via API
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome": "Teste Persistência", "email": "persistencia@test.com"}'

# 2. Reiniciar o container da API
docker-compose restart api

# 3. Listar clientes - dados devem persistir
curl http://localhost:8000/clientes
```

#### 4. Testes de Performance (Básico)

```bash
# Criar múltiplos clientes
for i in {1..100}; do
  curl -X POST http://localhost:8000/clientes \
    -H "Content-Type: application/json" \
    -d "{\"nome\": \"Cliente $i\", \"email\": \"cliente$i@email.com\"}" &
done

# Listar e medir tempo de resposta
time curl http://localhost:8000/clientes
```

#### 5. Monitoramento de Logs

```bash
# Logs em tempo real
docker-compose logs -f api

# Logs do PostgreSQL
docker-compose logs -f postgres
```

### Estratégia Completa de Validação

1. **Desenvolvimento:** Executar testes unitários continuamente
2. **Pré-commit:** Rodar todos os testes (`pytest`)
3. **Pós-deploy:** Executar smoke tests nos endpoints principais
4. **Monitoramento:** Verificar logs e métricas de performance
5. **Integração:** Validar conexão e persistência no banco de dados

## 💡 Soft Skills: Lidando com Mudanças de Requisitos

### Minha Abordagem para Mudanças de Requisitos

#### 1. **Comunicação Proativa**
- Sempre busco entender o **"porquê"** da mudança antes de implementar
- Questiono para garantir alinhamento: "Qual problema estamos resolvendo?"
- Documento as mudanças e seu impacto para manter todos informados

#### 2. **Avaliação de Impacto**
Quando recebo uma mudança de requisito, avalio:
- **Impacto técnico:** O que precisa ser alterado no código?
- **Impacto em funcionalidades existentes:** Algo vai quebrar?
- **Impacto em testes:** Quais testes precisam ser atualizados?
- **Impacto no cronograma:** Quanto tempo vai levar?

#### 3. **Arquitetura Flexível**
Projeto o código pensando em flexibilidade:
- **Separação de responsabilidades:** Facilita mudanças isoladas
- **Injeção de dependências:** Permite trocar implementações
- **Testes automatizados:** Garantem que mudanças não quebrem o existente
- **Código limpo:** Facilita entendimento e manutenção

#### 4. **Iteração e Feedback**
- Prefiro entregas incrementais para validar mudanças cedo
- Solicito feedback frequente: "Isso atende o que você esperava?"
- Estou aberto a ajustes baseados no feedback recebido

#### 5. **Exemplo Prático**

**Situação:** No meio do projeto, o time decide que precisa de busca por nome.

**Minha Resposta:**
1. ✅ **Entendi a necessidade:** "Queremos facilitar a busca de clientes"
2. ✅ **Avaliei o impacto:** "Preciso adicionar query param e método no service"
3. ✅ **Implementei com qualidade:** Código limpo + testes
4. ✅ **Documentei:** Atualizei o README com exemplos
5. ✅ **Validei:** Testei manualmente e automaticamente

#### 6. **Mindset de Crescimento**
- Vejo mudanças como **oportunidades de aprendizado**
- Sempre elenco os requisitos
- Não me apego emocionalmente ao código
- Entendo que mudanças fazem parte do desenvolvimento ágil
- Mantenho postura positiva e colaborativa

### Resumo da Abordagem

| Situação | Minha Ação |
|----------|------------|
| Requisito novo | Questiono o valor e avalio impacto |
| Mudança de prioridade | Reavalio planejamento e comunico |
| Feedback negativo | Ouço com mente aberta e busco melhorar |
| Incerteza técnica | Faço spike/POC antes de comprometer |
| Pressão de prazo | Comunico riscos e negocio escopo |

---

## 📝 Conclusão

Este projeto demonstra:
- ✅ Implementação de API REST com boas práticas
- ✅ Arquitetura em camadas bem definida
- ✅ Testes automatizados completos (unitários e integração)
- ✅ Documentação clara e exemplos práticos
- ✅ Containerização com Docker
- ✅ Validação robusta de dados
- ✅ Tratamento adequado de erros

## 👤 Autor

Gabriela Polli

Desenvolvido como teste técnico para a vaga de Analista de Engenharia Jr.
