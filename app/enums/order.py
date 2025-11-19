from enum import Enum


class OrderStatusEnum(str, Enum):
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    UNPAID = "unpaid"
    PICKED_UP = "picked_up"
    DELIVERED_TERMINAL = "delivered_terminal"
    NO_TITLE = "no_title"
    LOADED_INTO_CONTAINER = "loaded_into_container"


class InvoiceTypeEnum(str, Enum):
    NAVI_GRUPE_INVOICE = "navi_grupe_invoice"
    T_AUTOLOGISTIC_INVOICE = "t_autologistics_invoice"


class AppealMessageRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
