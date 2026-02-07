# infrastructure/adapters/in_memory_user_repository.py
from datetime import datetime
from typing import Dict, List, Optional
from domain.user import User, UserCreate, UserUpdate, UserStatus
from application.ports.user_repository import UserRepositoryPort

class InMemoryUserRepository(UserRepositoryPort):
    """Adaptador - Implementación con base de datos en memoria"""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._next_id: int = 1  # Contador para IDs consecutivos
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Inicializar con datos de ejemplo"""
        sample_users = [
            UserCreate(username="admin", email="admin@example.com"),
            UserCreate(username="user1", email="user1@example.com"),
        ]
        for user_data in sample_users:
            self.create(user_data)
    
    def create(self, user_data: UserCreate) -> User:
        # Generar ID consecutivo
        user_id = str(self._next_id)
        self._next_id += 1  # Incrementar para el próximo usuario
        
        user = User(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            status=UserStatus.ACTIVE,
            created_at=datetime.now()
        )
        self._users[user_id] = user
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def get_all(self) -> List[User]:
        return list(self._users.values())
    
    def update(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        user = self._users.get(user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        updated_user = user.model_copy(update=update_data)
        self._users[user_id] = updated_user
        return updated_user
    
    def delete(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False
    
    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None