from abc import ABC, abstractmethod
from typing import List, Optional
from domain.user import User, UserCreate, UserUpdate

class UserRepositoryPort(ABC):
    
    @abstractmethod
    def create(self, user_data: UserCreate) -> User:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[User]:
        pass
    
    @abstractmethod
    def update(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass