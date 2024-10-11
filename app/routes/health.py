from fastapi import APIRouter

router = APIRouter()

@router.get("/health_check", tags=["root"])
async def read_root() -> dict:
    return {"message": "FastApi is running"}