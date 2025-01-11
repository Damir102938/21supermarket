"""Этот модуль содержит конфигурацию приложения 'orders' для Django."""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Конфигурация приложения orders."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
