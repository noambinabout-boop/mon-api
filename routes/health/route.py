from fastapi import APIRouter

router = APIRouter(prefix="/health")


@router.get("/")
def health():
    return {"Status": "ok", "version": "2"}