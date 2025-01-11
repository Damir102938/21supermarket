"""Представления для приложения 'myShop'."""
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.utils.timezone import now


def get_published_products():
    """Фильтрация продуктов."""
    current_time = now()
    return Product.objects.filter(
        available=True,
        created__lte=current_time,
        hidden=False
    )


def product_list(request, category_slug=None):
    """Список продуктов."""
    category = None
    categories = Category.objects.all()
    products = get_published_products()
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    """Информация о продукте."""
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


def csrf_failure(request, reason=''):
    """403."""
    return render(request, '403csrf.html', status=403)


def page_not_found(request, exception):
    """404."""
    return render(request, '404.html', status=404)


def server_error(request):
    """500."""
    return render(request, '500.html', status=500)
