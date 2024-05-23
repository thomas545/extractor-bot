# Extractor Bot

### Instructions

### Installation/Setup
- Clone the repository

- Create Python ENV
  - python3 -m venv `env_name`
  - source  `env_name`/bin/activate
  - pip install -r requirements.txt
  - Add `.env` file with your secret keys that in `env_dev`

- Run project
  - Run: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` or `python main.py`

## API Documentation
- [Local Docs](http://127.0.0.1:8000/docs)

## Tech Stack:
- Python 3.10+
- FastAPI
- Langchain
- OpenAI / Gemini
- MongoDB
- Milvus
- uvicorn

### Endpoints usage

