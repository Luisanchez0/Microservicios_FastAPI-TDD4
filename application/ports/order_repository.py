from abc import ABC, abstractmethod
from typing import List, Optional
from domain.order import Order, OrderCreate, OrderUpdate

class OrderRepositoryPort(ABC):
    
    @abstractmethod
    def create(self, order_data: OrderCreate) -> Order:
        pass
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Order]:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: str) -> List[Order]:
        pass
    
    @abstractmethod
    def update(self, order_id: str, order_data: OrderUpdate) -> Optional[Order]:
        pass
    
    @abstractmethod
    def delete(self, order_id: str) -> bool:
        pass