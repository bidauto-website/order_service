from fastapi import APIRouter

container_router = APIRouter()

@container_router.get("/{container_id}")