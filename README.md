# HR RAG Chatbot
This project is a Retrieval-Augmented Generation (RAG) system that allows employees to ask questions about HR policies using natural language.

## Tech Stack
- Python
- FastAPI
- Qdrant
- LiteLLM
- Docker & Docker Compose

# Architecture
- FastAPI for API layer
- Qdrant as vector database
- Ingest service for document indexing

# How to Run
bash
docker compose build
docker compose up -d qdrant api
docker compose run ingest