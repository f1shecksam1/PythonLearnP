# 🧰 Stage 1: Development
FROM python:3.10-slim AS dev

WORKDIR /learnpyapp

COPY pyproject.toml README.md /learnpyapp/
COPY src /learnpyapp/src

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -e . \
    && pip install black ruff mypy pytest

CMD ["uvicorn", "learnpyapp.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 🚀 Stage 2: Production
FROM python:3.10-slim AS prod

WORKDIR /learnpyapp
COPY --from=dev /learnpyapp /learnpyapp

# Yalnızca gerekli runtime bağımlılıklarını yükle
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -e .

EXPOSE 8000
CMD ["uvicorn", "learnpyapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
