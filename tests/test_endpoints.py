import requests



def test_records_endpoint():
    url = "http://localhost:8000/records"
    payload = {
        "user_id": 2,
        "token": "c7b26ff2-d0c8-4894-888e-88f05e9450f2",
        "audio": ("audio.wav", open("path/to/audio.wav", "rb"), "audio/wav")
    }
    response = requests.post(url, files=payload)
    assert response.status_code == 200
    assert response.json()["success"] == True
    # Добавьте дополнительные проверки для ответа сервера

