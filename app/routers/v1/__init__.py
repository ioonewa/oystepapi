from .tiles import routers as tile_routers

from .events import router as event_router
from .links import router as links_router
from .selection import router as properties_router
from .feed import router as feed_router

from .user import router as user_router

routers = [
    *tile_routers,

    event_router,
    links_router,
    properties_router,
    feed_router,

    user_router
]

from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/v1",
    tags=['Production'],
    dependencies=[Depends(get_current_user)]
)

for r in routers:
    router.include_router(r)