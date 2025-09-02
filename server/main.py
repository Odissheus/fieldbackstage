from fastapi import FastAPI
from server.routers import auth, upload, insights, ci, reports, qa, admin
from server.routers import product_lines
from server.routers import analytics, processing
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from server.db import init_db
from server.config import settings
from server.processing_queue import start_worker_once
from server.ai_services import init_ai_services


app = FastAPI(title="React Field Insights API", version="1.0.0", openapi_url="/v1/openapi.json")
app.include_router(auth.router, prefix="/v1")
app.include_router(upload.router, prefix="/v1")
app.include_router(insights.router, prefix="/v1")
app.include_router(ci.router, prefix="/v1")
app.include_router(reports.router, prefix="/v1")
app.include_router(qa.router, prefix="/v1")
app.include_router(admin.router, prefix="/v1")
app.include_router(product_lines.router, prefix="/v1")
app.include_router(analytics.router, prefix="/v1")
app.include_router(processing.router, prefix="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.TRUSTED_HOSTS and settings.TRUSTED_HOSTS != ["*"]:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)
app.add_middleware(GZipMiddleware, minimum_size=1024)


@app.on_event("startup")
def on_startup():
    init_db()
    init_ai_services()
    start_worker_once()


@app.get("/healthz")
def health():
    return {"status": "ok"}

