# tests/conftest.py
# 🧩 pytest fixture dosyası — testlerde tekrar kullanılacak nesneleri burada tanımlar.

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from learnpyapp.main import app


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    🧱 FastAPI TestClient fixture’ı.
    scope="module" → Her test dosyasında bir kez oluşturulur.
    """
    with TestClient(app) as c:
        yield c
