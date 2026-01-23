# 🧰 Geliştirme ortamı için temel imaj (Stage 1)
FROM python:3.10-slim AS dev

WORKDIR /learnpyapp  # Çalışma dizini

# Temel dosyaları kopyala
COPY pyproject.toml README.md /learnpyapp/
COPY src /learnpyapp/src

# 📦 Gerekli bağımlılıkları yükle
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -e . \
    && pip install black ruff mypy pytest  # Geliştirme araçları

# 🚀 Uygulamayı başlat
CMD ["uvicorn", "learnpyapp.main:app", "--host", "0.0.0.0", "--port", "8000"]

# -----------------------------
# 🚀 Production ortamı (Stage 2)
FROM python:3.10-slim AS prod

WORKDIR /learnpyapp
COPY --from=dev /learnpyapp /learnpyapp

# Sadece çalışma zamanı bağımlılıklarını yükle
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -e .

EXPOSE 8000
CMD ["uvicorn", "learnpyapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
