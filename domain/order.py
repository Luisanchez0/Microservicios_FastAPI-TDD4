from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED" 
    CANCELLED = "CANCELLED"

class Order(BaseModel):
    id: str
    id_usuario: str
    producto: str
    cantidad: int = Field(gt=0)
    precio: float = Field(gt=0)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True


#pedido enviado
    def send(self):
        self.status = OrderStatus.SENT
        self.updated_at = datetime.now()

#pedido entregado
    def deliver(self):
        self.status = OrderStatus.DELIVERED
        self.updated_at = datetime.now()
    
#pedido cancelado
    def cancel(self):
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now()

#es enviado?
    def is_sent(self) -> bool:
        return self.status == OrderStatus.SENT
    
#entregado?
    def is_delivered(self) -> bool:
        return self.status == OrderStatus.DELIVERED
#cancelado?
    def is_cancelled(self) -> bool:
        return self.status == OrderStatus.CANCELLED
#pendiente?
    def is_pending(self) -> bool:
        return self.status == OrderStatus.PENDING
    
    def calculate_total(self) -> float:
        return self.cantidad * self.precio
    

class OrderCreate(BaseModel):
    id_usuario : str
    producto: str
    cantidad: int = Field(gt=0, description="debe ser mayor a cero")
    precio: float = Field(gt=0, description="debe ser mayor a cero")

class OrderUpdate(BaseModel):
    producto: Optional[str] = None
    cantidad: Optional[int] = Field(None, gt=0)
    precio: Optional[float] = Field(None, gt=0)
    status: Optional[OrderStatus] = None