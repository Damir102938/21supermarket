"""
Этот модуль содержит регистрацию моделей в Django Admin.

Здесь указаны настройки отображения и поиска для моделей 'Order' и
'DiscountCard'.
"""
from django.contrib import admin
from .models import Order, OrderItem, DiscountСard


class OrderItemInline(admin.TabularInline):
    """Встраиваемый интерфейс для элементов заказа (OrderItem)."""

    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Order."""

    list_display = ['id',
                    'created', 'updated', 'payment_method']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]


@admin.register(DiscountСard)
class DiscountСardAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели DiscountСard."""

    list_display = ['id', 'discount', 'created', 'updated']
    list_filter = ['created', 'updated']
    list_editable = ['discount']
