from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1 import routers
from app.core.config import settings

app = FastAPI()

Instrumentator().instrument(app).expose(app)

for router in routers:
    app.include_router(router, prefix=settings.api.prefix)

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/health")
def healthcheck():
    return {"status": "healthy"}

