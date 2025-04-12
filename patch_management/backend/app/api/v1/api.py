from fastapi import APIRouter
from app.api.v1.endpoints import (
    users,
    servers,
    patches,
    reports,
    analytics,
    auth
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(servers.router, prefix="/servers", tags=["servers"])
api_router.include_router(patches.router, prefix="/patches", tags=["patches"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"]) 