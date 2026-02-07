from typing import List
from fastapi import APIRouter, HTTPException, Depends
from domain.user import User, UserCreate, UserUpdate
from application.services.user_services import UserService
from infrastructure.adapters.in_memory_user_repository import InMemoryUserRepository

router = APIRouter(prefix="/api/users", tags=["Users"])

_user_repository = InMemoryUserRepository()

def get_user_service() -> UserService:
    return UserService(_user_repository)

@router.post("/", response_model=User, status_code=201)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        return service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[User])
def list_users(service: UserService = Depends(get_user_service)):
    return service.list_users()

@router.get("/active", response_model=List[User])
def list_active_users(service: UserService = Depends(get_user_service)):
    return service.list_active_users()

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: str,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    try:
        user = service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):

    if not service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

"""
@router.post("/{user_id}/activate", response_model=User)
def activate_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):
    user = service.activate_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/{user_id}/deactivate", response_model=User)
def deactivate_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):
    user = service.deactivate_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

    """