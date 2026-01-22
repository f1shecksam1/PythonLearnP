FROM python:3.10-slim

WORKDIR /learnpyapp

COPY pyproject.toml /learnpyapp/pyproject.toml
COPY README.md /learnpyapp/README.md
COPY src /learnpyapp/src

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -e .

CMD ["python", "-m", "learnpyapp"]
