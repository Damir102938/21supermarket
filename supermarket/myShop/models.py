"""Модели приложения myShop."""
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Модель для категорий."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        """Метаданные для модели Category."""

        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        """Возвращает название категории."""
        return self.name

    def get_absolute_url(self):
        """Возвращает абсолютный URL для категории."""
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    """Модель для продуктов."""

    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    hidden = models.BooleanField(default=False)

    class Meta:
        """Метаданные для модели Product."""

        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        """Возвращает название продукта."""
        return self.name

    def get_absolute_url(self):
        """Возвращает абсолютный URL для продукта."""
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
