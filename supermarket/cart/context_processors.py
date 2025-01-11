"""Контекстный процессор для приложения 'cart'."""
from .cart import Cart


def cart(request):
    """Контекстный процессор для корзины."""
    return {'cart': Cart(request)}
