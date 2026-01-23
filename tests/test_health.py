# tests/test_health.py
# 💓 Uygulamanın sağlık kontrolü (health endpoint) testleri

def test_health_endpoint(client):
    """
    ✅ /api/v1/health endpoint’inin doğru çalıştığını doğrular.
    """
    response = client.get("/api/v1/health")

    # HTTP 200 dönmeli
    assert response.status_code == 200

    # JSON yanıtı {"status": "ok"} olmalı
    assert response.json() == {"status": "ok"}
