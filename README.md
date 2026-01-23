# 🚀 LearnPyApp

Modern Python uygulamaları için üretim düzeyinde bir **FastAPI başlangıç şablonu**.

Temiz kod yapısı, güçlü tip güvenliği ve otomatik kalite kontrol araçları (Black, Ruff, Mypy, Pytest) içerir.  
Geliştirme ortamı Docker desteklidir, CI/CD ise GitHub Actions ile entegredir.

---

## 📦 Özellikler

✅ **FastAPI** – modern, yüksek performanslı API çatısı  
✅ **Pydantic Settings** – ortam değişkenlerinden güçlü config yönetimi  
✅ **Mypy** – zorunlu type hint denetimi  
✅ **Ruff** – ultra hızlı linting ve import sıralama  
✅ **Black** – otomatik kod biçimlendirme  
✅ **Pytest** – test framework’ü  
✅ **Docker** – kolay kurulum ve container tabanlı çalışma  
✅ **GitHub Actions** – otomatik kalite ve test kontrolü  

---

## 🧱 Proje Yapısı

```plaintext
src/
├── learnpyapp/
│   ├── api/               # API katmanı (v1, endpoints)
│   ├── core/              # Config, logging, request_id
│   ├── middlewares/       # Ortak middleware’ler
│   └── main.py            # Uygulama factory fonksiyonu

⚙️ Kurulum (Yerel Geliştirme)
1️⃣ Sanal ortam oluştur

python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

2️⃣ Bağımlılıkları yükle

pip install -e .
pip install black ruff mypy pytest

3️⃣ Çalıştır

uvicorn learnpyapp.main:app --reload

Tarayıcıdan:
👉 http://localhost:8000/docs
🧰 Kod Kalitesi Araçları
⚫ Black (Biçimlendirme)

Kodun PEP8 standartlarına göre otomatik biçimlendirilmesini sağlar:

black .

🪶 Ruff (Linting & Import Düzeni)

Kodda hatalı kalıplar, gereksiz import’lar veya biçim sorunlarını bulur:

ruff check . --fix

🔍 Mypy (Tip Güvenliği)

Tüm fonksiyonlarda type hint denetimi yapar:

mypy src/

Eğer type hint eksikse hata verir (örnek: disallow_untyped_defs = true).
🧪 Pytest (Testler)

Unit veya integration testleri çalıştırır:

pytest -q

🧱 Docker Kullanımı
1️⃣ Build ve Çalıştır

docker compose up --build

Uygulama: http://localhost:8000
2️⃣ Dockerfile (özet)

    Hafif python:3.10-slim imajı

    Geliştirme modunda black, ruff, mypy dahil edilebilir

    Production’da sade ve hızlı build

⚙️ CI/CD (GitHub Actions)

Otomatik kalite kontrol için .github/workflows/ci.yml dosyası içerir:

    ✅ Black → Kod formatı denetimi

    ✅ Ruff → Lint kontrolü

    ✅ Mypy → Type hint denetimi

    ✅ Pytest → Otomatik test çalıştırma

GitHub Actions, her push veya pull request işleminde bu adımları otomatik yürütür.
🧩 Ek Özellikler (Planlanabilir)

    PostgreSQL + SQLModel entegrasyonu

    JWT tabanlı authentication

    Sentry veya Prometheus ile izleme

    CI’de coverage raporu üretimi

    Pre-commit hook’lar (black, ruff, mypy)

🧠 Yararlı Komutlar
Amaç	Komut
Kod biçimlendirme	black .
Lint düzeltme	ruff check . --fix
Tip kontrolü	mypy src/
Test çalıştır	pytest -q
Docker build	docker build -t learnpyapp .
Docker çalıştır	docker run -p 8000:8000 learnpyapp
📜 Lisans

MIT License © 2026
Geliştirici: PythonLearnP