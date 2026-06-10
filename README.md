# HR RAG Bot

An AI-powered HR Knowledge Assistant built with Retrieval-Augmented Generation (RAG) to answer employee questions using company HR documents.

The system ingests PDF and DOCX files, converts them into embeddings, stores them in Qdrant Vector Database, retrieves the most relevant document chunks, and generates grounded responses using Large Language Models (LLMs).

---

## Features

* Retrieval-Augmented Generation (RAG)
* FastAPI REST API
* Semantic Search over HR Documents
* Qdrant Vector Database
* LiteLLM Integration
* PDF & DOCX Document Processing
* Automated Document Chunking
* Metadata Tracking
* Dockerized Deployment
* Unit Testing Support

---

## Architecture

```text
                HR Documents
             (PDF / DOCX Files)
                       │
                       ▼
                Document Loader
                       │
                       ▼
                 Text Chunking
                       │
                       ▼
                  Embeddings
                       │
                       ▼
               Qdrant Vector DB
                       │
                       ▼
Employee Question → Retrieval → Relevant Chunks
                                       │
                                       ▼
                                 LiteLLM
                                       │
                                       ▼
                               Final Answer
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### AI & RAG

* LiteLLM
* Vector Embeddings
* Semantic Search
* Retrieval-Augmented Generation (RAG)

### Vector Database

* Qdrant

### Document Processing

* PyPDF2
* python-docx
* LangChain Text Splitters

### DevOps

* Docker
* Docker Compose

### Testing

* Pytest

---

## Project Structure

```text
hr-rag-bot/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── security.py
│   └── services/
│       ├── embeddings.py
│       ├── retrieval.py
│       └── llm.py
│
├── ingest/
│   ├── ingest.py
│   ├── chunker.py
│   └── loaders/
│       ├── pdf_loader.py
│       └── docx_loader.py
│
├── data/hr_docs/
│   ├── PDF documents
│   ├── DOCX documents
│   └── metadata.json
│
├── qdrant/
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## How It Works

### 1. Document Ingestion

The ingestion pipeline:

* Loads HR documents from PDF and DOCX files.
* Splits documents into smaller chunks.
* Generates embeddings for each chunk.
* Stores vectors and metadata in Qdrant.

### 2. Question Answering

When a user asks a question:

1. The query is converted into an embedding.
2. Similar vectors are retrieved from Qdrant.
3. Relevant context is collected.
4. LiteLLM generates an answer using the retrieved information.
5. The response is returned through the FastAPI API.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Fatemeh127/hr-rag-bot.git
cd hr-rag-bot
```

### Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
QDRANT_URL=http://localhost:6333
EMPLOYEE_API_KEY=your_key
MANAGER_API_KEY=your_key
ADMIN_API_KEY=your_key
```

---

## Run Qdrant

```bash
docker compose up -d
```

---

## Ingest Documents

```bash
python -m ingest.ingest
```

---

## Start API

```bash
uvicorn app.main:app --reload
```

API will be available at:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Example Request

```http
POST /ask
```

Request:

```json
{
  "question": "How many vacation days do employees receive?"
}
```

Response:

```json
{
  "answer": "Employees receive 25 annual vacation days according to the HR policy."
}
```

---

## Future Improvements

* Authentication & Authorization
* Role-Based Access Control (RBAC)
* Hybrid Search (Keyword + Vector Search)
* Response Caching
* Conversation Memory
* Evaluation Framework
* Multi-Collection Support
* Monitoring & Observability

---

## Learning Outcomes

This project demonstrates practical experience with:

* Building RAG pipelines
* FastAPI backend development
* Vector databases
* Semantic search systems
* LLM integration
* Dockerized AI applications
* Document processing workflows

---

## Author

**Fatemeh Abidizadegan**
