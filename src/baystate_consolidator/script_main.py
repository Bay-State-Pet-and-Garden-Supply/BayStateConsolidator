from fastapi import FastAPI
from baystate_consolidator.api.routes import router

app = FastAPI(title="BayStateConsolidator")

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
