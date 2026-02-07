from typing import List, Optional
from domain.user import User, UserCreate, UserUpdate
from application.ports.user_repository import UserRepositoryPort

class UserService:
    
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository
    
    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"El email {user_data.email} ya está registrado")
        
        return self.user_repository.create(user_data)
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)
    
    def list_users(self) -> List[User]:
        return self.user_repository.get_all()
    
    def list_active_users(self) -> List[User]:
        all_users = self.user_repository.get_all()
        return [user for user in all_users if user.is_active()]
    
    def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        if user_data.email and user_data.email != user.email:
            existing_user = self.user_repository.get_by_email(user_data.email)
            if existing_user:
                raise ValueError(f"El email {user_data.email} ya está registrado")
        
        return self.user_repository.update(user_id, user_data)
    
    def delete_user(self, user_id: str) -> bool:
        return self.user_repository.delete(user_id)
    
    def activate_user(self, user_id: str) -> Optional[User]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        user.activate()
        return self.user_repository.update(user_id, UserUpdate(status=user.status))
    
    def deactivate_user(self, user_id: str) -> Optional[User]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        user.deactivate()
        return self.user_repository.update(user_id, UserUpdate(status=user.status))