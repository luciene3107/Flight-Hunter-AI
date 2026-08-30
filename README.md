# Flight Hunter AI ✈️

API de um agente inteligente para **monitoramento de passagens aéreas**. O sistema
guarda buscas de voo, verifica os preços periodicamente e envia um alerta no
**Telegram** quando encontra uma passagem dentro do teto de preço definido.

---

## Funcionalidades

- **API REST** (FastAPI) para cadastrar e listar buscas de voo.
- **Agente de voos** que monta um plano de busca a partir da requisição
  (`FlightAgent` → `FlightPlanner` → `FlightTools`) e, opcionalmente, extrai os
  parâmetros de uma frase em linguagem natural usando um LLM na Groq
  (`llama-3.3-70b-versatile` via LangChain).
- **Provedor de dados**: SerpApi (engine `google_flights`), com _fallback_
  automático para um `MockProvider` quando a SerpApi não retorna resultados.
- **Busca flexível** por região (ex.: Europa), gerando combinações de destino e
  data a partir de um catálogo de aeroportos.
- **Monitoramento automático** a cada 6 horas via APScheduler.
- **Alertas no Telegram** com deduplicação inteligente: o mesmo voo só é
  reenviado se o preço cair ou se já tiverem se passado 24 horas desde o último
  alerta.
- Persistência em **PostgreSQL** via SQLAlchemy.

---

## Stack

| Camada        | Tecnologia                                   |
|---------------|----------------------------------------------|
| API           | FastAPI + Uvicorn                            |
| Agendador     | APScheduler (`BackgroundScheduler`)          |
| Banco         | PostgreSQL + SQLAlchemy 2.x                  |
| LLM           | Groq + LangChain (`langchain-groq`)          |
| Dados de voo  | SerpApi (Google Flights) / MockProvider     |
| Notificações  | Telegram Bot API                            |

---

## Estrutura do projeto

```
app/
├── main.py                  # App FastAPI, ciclo de vida e rotas
├── agents/                  # Agente, planner e tools de busca
├── llm/                     # Cliente Groq e extrator de linguagem natural
├── providers/               # SerpApi, MockProvider e parsers
├── services/                # FlightService, TelegramService, EuropeSearchService
├── repositories/            # Acesso a dados (buscas e alertas enviados)
├── models/                  # Modelos SQLAlchemy (flight_searches, flight_alerts)
├── schemas/                 # Schemas Pydantic (entrada/saída da API)
├── scheduler/               # runner.py (agendamento) e tasks.py (rotina)
├── catalog/                 # Catálogo de destinos/aeroportos
└── core/                    # config.py, logger.py
init_db.py                   # Cria as tabelas manualmente
tests/                       # Scripts de verificação
```

---

## Pré-requisitos

- Python 3.12+
- PostgreSQL (ou Docker, para subir via `docker-compose`)
- Conta na [SerpApi](https://serpapi.com/) (chave de API)
- Bot do Telegram e o `chat_id` do destinatário
- Chave de API da [Groq](https://console.groq.com/) (apenas para busca por
  linguagem natural)

---

## Configuração

Crie um arquivo `.env` na raiz:

```env
# Banco
DATABASE_URL=postgresql://flight:flight123@localhost:5432/flight_hunter

# Telegram
TELEGRAM_BOT_TOKEN=seu_token_do_botfather
TELEGRAM_CHAT_ID=seu_chat_id

# SerpApi
SERPAPI_API_KEY=sua_chave_serpapi

# LLM (Groq) - necessário só para extração de linguagem natural
GROQ_API_KEY=sua_chave_groq
MODEL_NAME=llama-3.3-70b-versatile
```

---

## Como rodar

### 1. Subir o banco com Docker

```bash
docker compose up -d postgres
```

### 2. Instalar as dependências

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

### 3. Criar as tabelas

As tabelas são criadas automaticamente quando a API sobe (`Base.metadata.create_all`
no ciclo de vida). Para criar manualmente:

```bash
python init_db.py
```

### 4. Iniciar a API

```bash
uvicorn app.main:app --reload
```

- API: <http://localhost:8000>
- Documentação interativa (Swagger): <http://localhost:8000/docs>

### Rodar tudo em container

```bash
docker build -t flight-hunter-ai .
docker run --env-file .env -p 8000:8000 flight-hunter-ai
```

---

## Endpoints

| Método | Rota         | Descrição                                              |
|--------|--------------|-------------------------------------------------------|
| `GET`  | `/`          | Healthcheck.                                          |
| `POST` | `/search`    | Executa uma busca com o agente e **salva** o monitoramento. |
| `GET`  | `/searches`  | Lista todos os monitoramentos cadastrados.            |

### Exemplo — `POST /search`

```json
{
  "search_type": "specific",
  "origin": "GRU",
  "destination": "MAD",
  "departure_date": "2026-10-01",
  "return_date": "2026-10-15",
  "max_price": 3500
}
```

Para busca flexível por região, use `"search_type": "flexible"`, `"region": "Europe"`
e `"months": 6` (nº de meses à frente a considerar).

Resposta:

```json
{
  "message": "3 voo(s) encontrado(s)",
  "max_price": 3500,
  "flights": [ /* ... */ ]
}
```

---

## Monitoramento automático

- Configurado em `app/scheduler/runner.py`: intervalo fixo de **6 horas**
  (`trigger="interval", hours=6`). A primeira execução ocorre 6h após a API subir.
- A rotina `check_flights_job` (`app/scheduler/tasks.py`):
  1. carrega os monitoramentos salvos;
  2. **filtra apenas destinos `MAD` (Madri) e `FCO` (Roma)** — ajuste essa lista no
     código para monitorar outras rotas;
  3. busca os voos e, para cada resultado, decide se envia alerta.

### Deduplicação de alertas

A tabela `flight_alerts` registra cada alerta enviado. Antes de notificar,
`FlightAlertRepository.should_alert()` reenvia o alerta quando:

- **não há alerta anterior** para aquele voo/origem/destino/data; **ou**
- o **preço atual é menor** que o do último alerta (queda de preço); **ou**
- já se passaram **≥ 24 h** (`COOLDOWN`) desde o último alerta.

Para "recomeçar do zero" e reenviar todos os alertas:

```sql
TRUNCATE TABLE flight_alerts RESTART IDENTITY;
```

---

## Testes

Os arquivos em `tests/` são scripts de verificação manual (executam buscas reais).
Rode individualmente, por exemplo:

```bash
python -m tests.test_flight_service
```

---

## Notas

- Sem `SERPAPI_API_KEY` válida, o `MockProvider` assume e retorna dados fictícios.
- O agendamento vive em memória: reiniciar a API zera a contagem do intervalo.
- Moeda, idioma e país das buscas estão fixos em `app/core/config.py`
  (`BRL` / `pt-BR` / `br`).
