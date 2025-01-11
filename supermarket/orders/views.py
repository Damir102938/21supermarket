"""Представления для приложения 'orders'."""
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem, Order, DiscountСard
from .forms import OrderCreateForm
from cart.cart import Cart
from django.utils.timezone import now
import random


def order_create(request):
    """Создание заказа."""
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.payment_method = form.cleaned_data['payment_method']

            discount_card_id = form.cleaned_data.get('discount_card_id')
            if discount_card_id:
                try:
                    discount_card = DiscountСard.objects.get(
                        id=discount_card_id)
                    total_cost = sum(
                        item['price'] * item['quantity'] for item in cart)
                    discounted_cost = discount_card.get_cost_discount(
                        total_cost)
                    order.total_cost = discounted_cost
                except DiscountСard.DoesNotExist:
                    order.total_cost = sum(
                        item['price'] * item['quantity'] for item in cart)
            else:
                order.total_cost = sum(
                    item['price'] * item['quantity'] for item in cart)

            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('orders:order_success'))
    else:
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})


def order_success(request):
    """Отображение чека."""
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)

    discount = round((1 - order.total_cost/order.get_total_cost())*100)
    discount = int(discount)

    receipt_data = {
        'order_id': order.id,
        'total_cost': order.total_cost,
        'cash_register': random.randint(1, 20),
        'order_items': order.items.all(),
        'order_time': now().strftime('%d-%m-%Y %H:%M:%S'),
        'transport_company': random.choice(
            ['Transport Company 1', 'Transport Company 2',
             'Transport Company 3', 'Transport Company 4',
             'Transport Company 5']),
        'payment_method': order.payment_method,
        'discount': discount,
    }

    return render(request, 'orders/order/success.html', receipt_data)
