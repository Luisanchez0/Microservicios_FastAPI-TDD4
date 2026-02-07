# infrastructure/api/order_routes.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from domain.order import Order, OrderCreate, OrderUpdate
from application.services.order_service import OrderService  
from infrastructure.adapters.in_memory_order_repository import InMemoryOrderRepository

router = APIRouter(prefix="/api/orders", tags=["Orders"])

# Singleton del repositorio (para mantener los datos en memoria)
_order_repository = InMemoryOrderRepository()

def get_order_service() -> OrderService:
    """Dependency injection"""
    return OrderService(_order_repository)

@router.post("/", response_model=Order, status_code=201)
def create_order(
    order_data: OrderCreate,
    service: OrderService = Depends(get_order_service)
):
    """Crear un nuevo pedido"""
    try:
        return service.create_order(order_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Order])
def list_orders(service: OrderService = Depends(get_order_service)):
    """Listar todos los pedidos"""
    return service.list_orders()

@router.get("/user/{user_id}", response_model=List[Order])
def list_user_orders(
    user_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Listar pedidos de un usuario específico"""
    return service.list_user_orders(user_id)

@router.get("/{order_id}", response_model=Order)
def get_order(
    order_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Obtener un pedido por ID"""
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order

@router.get("/{order_id}/total")
def get_order_total(
    order_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Obtener el total de un pedido"""
    total = service.get_order_total(order_id)
    if total is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"order_id": order_id, "total": total}

@router.put("/{order_id}", response_model=Order)
def update_order(
    order_id: str,
    order_data: OrderUpdate,
    service: OrderService = Depends(get_order_service)
):
    """Actualizar un pedido"""
    try:
        order = service.update_order(order_id, order_data)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Eliminar un pedido"""
    if not service.delete_order(order_id):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

@router.post("/{order_id}/send", response_model=Order)
def send_order(
    order_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Marcar pedido como enviado"""
    order = service.send_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order

@router.post("/{order_id}/deliver", response_model=Order)
def deliver_order(
    order_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Marcar pedido como entregado"""
    order = service.deliver_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order

@router.post("/{order_id}/cancel", response_model=Order)
def cancel_order(
    order_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Cancelar pedido"""
    order = service.cancel_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order