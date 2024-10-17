from sqlalchemy import Enum


class PaymentStatus(Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
