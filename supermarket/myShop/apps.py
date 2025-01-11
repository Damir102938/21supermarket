"""Этот модуль содержит конфигурацию приложения 'myShop' для Django."""
from django.apps import AppConfig


class MyshopConfig(AppConfig):
    """Конфигурация приложения myShop."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myShop'
