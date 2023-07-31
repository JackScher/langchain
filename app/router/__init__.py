from fastapi import APIRouter
from .assistant import assistant_router

router = APIRouter(prefix="/api")
router.include_router(assistant_router)
