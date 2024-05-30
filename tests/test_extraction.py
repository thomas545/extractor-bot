from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_headers():
    return {"Content-Type": "application/json"}


body = {"email": "test@gmail.com", "password": "123456thomas"}
response = client.post("/auth/login/", json=body, headers=get_headers())
access_token = response.json().get("data", {}).get("access_token", "")


def test_upload_api():
    files = [
        (
            "files",
            (
                "東京都建築安全条例.pdf",
                open(
                    "/Users/thomas/Downloads/SSD-AI-Assignment 3/sample/東京都建築安全条例.pdf",
                    "rb",
                ),
                "application/pdf",
            ),
        ),
        (
            "files",
            (
                "建築基準法施行令.pdf",
                open(
                    "/Users/thomas/Downloads/SSD-AI-Assignment 3/sample/建築基準法施行令.pdf",
                    "rb",
                ),
                "application/pdf",
            ),
        ),
    ]

    upload_headers = {"Authorization": f"Bearer {access_token}"}
    upload_response = client.post("/upload/", files=files, headers=upload_headers)
    assert upload_response.status_code == 201
    assert upload_response.json().get("status") == "success"
    assert len(upload_response.json().get("data", [])) == len(files)


def test_ocr_api():
    headers = get_headers()
    # body = {"email": "test@gmail.com", "password": "123456thomas"}
    # response = client.post("/auth/login/", json=body, headers=headers)
    # access_token = response.json().get("data", {}).get("access_token", "")

    ocr_body = {
        # "file_id": "6654c225e8769fc30206f225"
        "url": "https://testingzone021.b-cdn.net/users_files/6651fbad0b03b201a830642a/1b38aa42-7a34-4bc9-b5fc-01c4e5f2c139.json"
    }
    headers.update({"Authorization": f"Bearer {access_token}"})
    ocr_response = client.post("/ocr/", json=ocr_body, headers=headers)
    assert ocr_response.status_code == 200
    assert ocr_response.json().get("status") == "success"
    assert ocr_response.json().get("data", {}).get("msg") == "Processing OCR File."


def test_extractor_api():
    headers = get_headers()
    extractor_body = {
        "file_id": "6654c225e8769fc30206f225",
        "query": "道路状に造られた敷地の頂点の角の長さはどれくらいですか",
    }

    headers.update({"Authorization": f"Bearer {access_token}"})
    extractor_response = client.post("/extract/", json=extractor_body, headers=headers)
    assert extractor_response.status_code == 200
    assert extractor_response.json().get("status") == "success"
    assert extractor_response.json().get("data", {}).get("response", "") is not None
