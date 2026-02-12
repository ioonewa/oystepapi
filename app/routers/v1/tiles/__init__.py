
from .education import router as education_router

routers = [
    education_router
]

from fastapi import APIRouter

router = APIRouter(prefix="", tags="modules")

for r in routers:
    router.include_router(router)