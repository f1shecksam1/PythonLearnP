# tests/conftest.py
# 🧩 Bu dosya pytest için ortak fixture’ları tanımlar.
# FastAPI test client oluşturup, testler arasında paylaşılmasını sağlar.

import pytest
from fastapi.testclient import TestClient

from learnpyapp.main import app  # Ana uygulama nesnesini içe aktarıyoruz


@pytest.fixture(scope="module")
def client() -> TestClient:
    """
    🧱 FastAPI TestClient fixture’ı.
    Her test dosyasında aynı client kullanılabilir.
    scope="module" → Her dosya için bir kez oluşturulur.
    """
    with TestClient(app) as c:
        yield c
