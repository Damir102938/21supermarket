"""Форма для оформления заказа."""
from django import forms
from .models import Order, DiscountСard


class OrderCreateForm(forms.ModelForm):
    """Форма для создания заказа."""

    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        label="",
    )

    discount_card_id = forms.DecimalField(
        max_digits=10,
        decimal_places=0,
        required=False,
        label="Discount card"
    )

    class Meta:
        """Метаданные для формы."""

        model = Order
        fields = ['payment_method']

    def save(self, commit=True):
        """Переопределяем метод save для обработки дисконтной карты."""
        order = super().save(commit=False)

        # Обработка номера дисконтной карты
        discount_card_id = self.cleaned_data.get('discount_card_id')
        if discount_card_id:
            try:
                # Проверяем наличие карты
                discount_card = DiscountСard.objects.get(id=discount_card_id)
                # Считаем стоимость заказа с учетом скидки
                order.total_cost = discount_card.get_cost_discount(
                    order.get_total_cost())
            except DiscountСard.DoesNotExist:
                # Если карта не найдена, продолжаем без применения скидки
                pass

        if commit:
            order.save()
        return order
