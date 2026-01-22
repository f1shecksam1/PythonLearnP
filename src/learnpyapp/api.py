from fastapi import FastAPI

app = FastAPI(title="learnpyapp")

@app.get("/health")
def health():
    return {"status": "ok"}
