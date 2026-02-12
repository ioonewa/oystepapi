from .v1 import router as v1_router
# from .test import router as test_router

from .auth import router as auth_router

from fastapi import APIRouter

router = APIRouter()

router.include_router(v1_router)
router.include_router(auth_router)