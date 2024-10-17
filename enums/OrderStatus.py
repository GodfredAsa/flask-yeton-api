from sqlalchemy import Enum


class OrderStatus(Enum):
    COMPLETED = 'COMPLETED'
    PENDING = 'PENDING'
    CANCELLED = 'CANCELLED'

