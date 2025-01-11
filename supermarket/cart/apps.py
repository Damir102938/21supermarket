"""Этот модуль содержит конфигурацию приложения 'cart' для Django."""
from django.apps import AppConfig


class CartConfig(AppConfig):
    """Конфигурация приложения Cart."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
