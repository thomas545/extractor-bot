# Extractor Bot

### Instructions

### Installation/Setup
- Clone the repository
- Install [MongoDB](https://www.mongodb.com/docs/manual/administration/install-community/) locally: 
- Install Python 3.10+
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

#### **File `Upload` Endpoint**
- Path: `/upload`
- Method: `POST` 
- Usage:
  - Accepts one or more file uploads (limited to pdf, tiff, png,jpeg formats).
  - Returns a list of file identifiers or signed URLs for the uploaded files.

- **Request**:

```
  files: form-data
```

- **Response**:

```
{
    "data": [
        {
            "_id": "6654c225e8769fc30206f225",
            "file_name": "東京都建築安全条例.json",
            "url": "https://testingzone021.b-cdn.net/users_files/6651fbad0b03b201a830642a/1b38aa42-7a34-4bc9-b5fc-01c4e5f2c139.json",
            "file_type": "json"
        }
    ],
    "status": "success",
    "status_code": 201
}
```

#### **`OCR` Endpoint**
- Path: /ocr
     
- Method: POST 
- Usage:
  - Add OCR file url or file upload `_id`.
  - Processing OCR results with embedding models, then upload the embeddings to a vector db for better searches.
  - Return File data to pass it to the extractor


- **Request**:

```
  {
    "file_id": "6654c225e8769fc30206f225"
    // "url": "https://testingzone021.b-cdn.net/users_files/6651fbad0b03b201a830642a/1b38aa42-7a34-4bc9-b5fc-01c4e5f2c139.json"
  }
```

- **Response**:

```
{
    "data": {
        "file": {
            "_id": "6654c225e8769fc30206f225",
            "file_name": "東京都建築安全条例.json",
            "url": "https://testingzone021.b-cdn.net/users_files/6651fbad0b03b201a830642a/1b38aa42-7a34-4bc9-b5fc-01c4e5f2c139.json",
            "file_type": "json"
        },
        "msg": "Processing OCR File."
    },
    "status": "success",
    "status_code": 200
}
```


#### **`Extraction` Endpoint**

- Path: /extract
- Method: POST 
- Usage:
  - Takes a query text and file_id as input.
  - Return response from the AI model depend on document data.



- **Request**:

```
  {
    "file_id": "6654c225e8769fc30206f225",
    "query": "道路状に造られた敷地の頂点の角の長さはどれくらいですか"
  }

```

- **Response**:

```
{
    "data": {
        "response": {
            "_id": "66575283f8f024a09219a037",
            "user_id": "6651fbad0b03b201a830642a",
            "file_id": "6654c225e8769fc30206f225",
            "query": "道路状に造られた敷地の頂点の角の長さはどれくらいですか",
            "response": "道路状に造られた敷地の頂点の角の長さは、長さニメートルの底辺を有する二等辺三角形の部分です。",
            "created_at": "2024-05-29T16:03:37Z",
            "updated_at": "2024-05-29T16:03:37Z"
        }
    },
    "status": "success",
    "status_code": 200
}
```

