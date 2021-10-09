from decimal import Context, Decimal, setcontext

import shortuuid


def generate_short_uuid():
    """Генерация 8ми значного уникального номера"""
    return shortuuid.uuid()[:8]


def set_context_for_decimal(currency_format, rounding_method):
    """Настройка контекста для работы с копейками"""
    currency = Context(rounding=rounding_method)
    setcontext(currency)
    coins_format = Decimal(currency_format)
    return coins_format



