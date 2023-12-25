from fastapi import APIRouter

from src.api.v1.endpoints import dishes, menus, submenus

api_router = APIRouter()
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(submenus.router)
api_router.include_router(dishes.router)
