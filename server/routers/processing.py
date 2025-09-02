from fastapi import APIRouter

router = APIRouter(tags=["processing"])

# Placeholder per health/status pipeline (futuro: coda, worker, metrics)
@router.get('/processing/health')
def processing_health():
    return {"pipeline": "ok"}

