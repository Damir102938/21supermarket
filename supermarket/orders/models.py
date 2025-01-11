"""Модели приложения orders."""
from django.db import models
from myShop.models import Product


class CommonInfo(models.Model):
    """
    Абстрактная модель, содержащая общие поля для других моделей.

    updated и created.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Метаданные для модели CommonInfo."""

        abstract = True


class Order(CommonInfo):
    """Модель заказа."""

    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('online', 'Online'),
    ]
    total_cost = models.DecimalField(max_digits=10,
                                     decimal_places=2, default=0)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default=''
    )

    class Meta:
        """Метаданные для модели Order."""

        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        """Возвращает строковое представление заказа."""
        return f'Order {self.id}'

    def get_total_cost(self):
        """Подсчитывает общую стоимость заказа."""
        return sum(
            item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Модель элемента заказа."""

    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """Возвращает строковое представление элемента заказа."""
        return str(self.id)

    def get_cost(self):
        """Подсчитывает стоимость данного элемента."""
        return self.price * self.quantity


class DiscountСard(CommonInfo):
    """Модель дисконтной карты."""

    id = models.DecimalField(max_digits=10,
                             decimal_places=0,
                             primary_key=True)
    discount = models.DecimalField(max_digits=3,
                                   decimal_places=0)

    class Meta:
        """Метаданные для модели DiscountСard."""

        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        """Возвращает строковое представление дисконтной карты."""
        return str(self.id)

    def get_cost_discount(self, total_cost):
        """Подсчитывает стоимость с учетом скидки."""
        return (100 - self.discount) * total_cost / 100
