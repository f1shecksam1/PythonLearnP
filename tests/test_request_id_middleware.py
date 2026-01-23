# tests/test_request_id_middleware.py
# 🧩 RequestIdMiddleware davranışını test eder.
# Amacımız: her istekte response header'ında "X-Request-ID" olmalı
#           ve header varsa aynen korunmalı.

from fastapi.testclient import TestClient

from learnpyapp.main import app


def test_request_id_auto_generated() -> None:
    """
    ✅ Header gönderilmediğinde middleware otomatik bir X-Request-ID üretmelidir.
    """
    client = TestClient(app)
    response = client.get("/api/v1/health")

    # Header'da "X-Request-ID" olmalı
    assert "X-Request-ID" in response.headers

    # Değer boş olmamalı
    request_id = response.headers["X-Request-ID"]
    assert isinstance(request_id, str)
    assert len(request_id) > 0


def test_request_id_preserved_from_header() -> None:
    """
    ✅ Eğer istek zaten X-Request-ID içeriyorsa,
       middleware aynı değeri response’a yansıtmalıdır.
    """
    client = TestClient(app)
    custom_id = "12345abcde"

    response = client.get("/api/v1/health", headers={"X-Request-ID": custom_id})

    # Response header'ındaki ID bizim gönderdiğimizle aynı olmalı
    assert response.headers.get("X-Request-ID") == custom_id
