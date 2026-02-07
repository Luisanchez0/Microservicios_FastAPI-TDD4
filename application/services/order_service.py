# application/services/order_service.py  (sin 's' al final)
from typing import List, Optional
from domain.order import Order, OrderCreate, OrderUpdate, OrderStatus
from application.ports.order_repository import OrderRepositoryPort

class OrderService:
    """Servicio de aplicación - Casos de uso de pedidos"""
    
    def __init__(self, order_repository: OrderRepositoryPort):
        self.order_repository = order_repository
    
    def create_order(self, order_data: OrderCreate) -> Order:
        """Crear un nuevo pedido"""
        return self.order_repository.create(order_data)
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Obtener pedido por ID"""
        return self.order_repository.get_by_id(order_id)
    
    def list_orders(self) -> List[Order]:
        """Listar todos los pedidos"""
        return self.order_repository.get_all()
    
    def list_user_orders(self, user_id: str) -> List[Order]:
        """Listar pedidos de un usuario"""
        return self.order_repository.get_by_user(user_id)
    
    def update_order(self, order_id: str, order_data: OrderUpdate) -> Optional[Order]:
        """Actualizar pedido"""
        return self.order_repository.update(order_id, order_data)
    
    def delete_order(self, order_id: str) -> bool:
        """Eliminar pedido"""
        return self.order_repository.delete(order_id)
    
    def send_order(self, order_id: str) -> Optional[Order]:
        """Marcar pedido como enviado"""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return None
        
        order.send()
        return self.order_repository.update(order_id, OrderUpdate(status=order.status))
    
    def deliver_order(self, order_id: str) -> Optional[Order]:
        """Marcar pedido como entregado"""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return None
        
        order.deliver()
        return self.order_repository.update(order_id, OrderUpdate(status=order.status))
    
    def cancel_order(self, order_id: str) -> Optional[Order]:
        """Cancelar pedido"""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return None
        
        order.cancel()
        return self.order_repository.update(order_id, OrderUpdate(status=order.status))
    
    def get_order_total(self, order_id: str) -> Optional[float]:
        """Obtener el total de un pedido"""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return None
        return order.calculate_total()