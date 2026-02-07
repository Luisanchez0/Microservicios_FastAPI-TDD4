# infrastructure/adapters/in_memory_order_repository.py
from datetime import datetime
from typing import Dict, List, Optional
from domain.order import Order, OrderCreate, OrderUpdate, OrderStatus
from application.ports.order_repository import OrderRepositoryPort

class InMemoryOrderRepository(OrderRepositoryPort):
    """Adaptador - Implementación con base de datos en memoria para pedidos"""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
        self._next_id: int = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Inicializar con datos de ejemplo"""
        sample_orders = [
            OrderCreate(id_usuario="1", producto="Laptop", cantidad=1, precio=1200.00),
            OrderCreate(id_usuario="1", producto="Mouse", cantidad=2, precio=25.50),
            OrderCreate(id_usuario="2", producto="Teclado", cantidad=1, precio=75.00),
        ]
        for order_data in sample_orders:
            self.create(order_data)
    
    def create(self, order_data: OrderCreate) -> Order:
        order_id = str(self._next_id)
        self._next_id += 1
        
        order = Order(
            id=order_id,
            id_usuario=order_data.id_usuario,
            producto=order_data.producto,
            cantidad=order_data.cantidad,
            precio=order_data.precio,
            status=OrderStatus.PENDING,
            created_at=datetime.now()
        )
        self._orders[order_id] = order
        return order
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
    
    def get_all(self) -> List[Order]:
        return list(self._orders.values())
    
    def get_by_user(self, user_id: str) -> List[Order]:
        return [order for order in self._orders.values() if order.id_usuario == user_id]
    
    def update(self, order_id: str, order_data: OrderUpdate) -> Optional[Order]:
        order = self._orders.get(order_id)
        if not order:
            return None
        
        update_data = order_data.model_dump(exclude_unset=True)
        update_data['updated_at'] = datetime.now()
        updated_order = order.model_copy(update=update_data)
        self._orders[order_id] = updated_order
        return updated_order
    
    def delete(self, order_id: str) -> bool:
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False