# 🛝 embedding-model-test-playground
![Image](https://github.com/user-attachments/assets/37b328cd-dd15-46c5-b703-929bee76eee0)

## Overview
This project is a playground for testing and comparing different embedding models using LangChain. It provides an environment to experiment with vector databases and embedding models.

## Features
- **Multiple Embedding Model Support**
  - Clova AI Embedding Model
    - Model: `bge-m3`
    - Provider: Naver Clova Studio
  - OpenAI Embedding Model
    - Model: `text-embedding-3-large`
    - Provider: OpenAI
- **Vector Search Capabilities**
  - Top-K Search (Default: Top-3)
  - Similarity-based search results with score
  - In-memory vector store implementation
- **Easy Testing Environment**
  - Docker-based execution environment
  - Intuitive UI through Streamlit

## Getting Started
### Server (Docker)
```bash
# Run Docker container
docker-compose up -d
```

### Local Development
```bash
# Run Streamlit server
streamlit run server.py
```

## Requirements
- Python 3.8 or higher
- Docker & Docker Compose
- OpenAI API Key
- Naver Clova Studio API Key

## Configuration
Set up the following environment variables in `.env` file:
You can refer to `.env.sample` file for the required environment variables.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).