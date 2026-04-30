from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator


def main_page(request, category_id=None):
    # Отримуємо всі категорії для бокового меню
    categories = Category.objects.all()
    current_category = None

    # Фільтрація за категорією
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)

        # --- РОЗУМНА ФІЛЬТРАЦІЯ ---
        # Створюємо список: натиснута категорія + всі її підкатегорії
        categories_list = [current_category] + list(current_category.subcategories.all())

        # Шукаємо товари, які належать БУДЬ-ЯКІЙ категорії з цього списку
        products_list = Product.objects.filter(category__in=categories_list).order_by('-created_at')
    else:
        # Якщо категорія не обрана - показуємо всі товари (найновіші зверху)
        products_list = Product.objects.all().order_by('-created_at')

    # Пагінація (по 9 товарів на сторінку)
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    })


# Функції для статичних сторінок (Як замовити, Доставка тощо)
def page_tree(request):
    categories = Category.objects.all()
    return render(request, 'shop/page1.html', {'categories': categories})


def page_two(request):
    categories = Category.objects.all()
    return render(request, 'shop/page2.html', {'categories': categories})


def page_contacts(request):
    categories = Category.objects.all()
    return render(request, 'shop/page3.html', {'categories': categories})


def page_cabinet(request):
    categories = Category.objects.all()
    return render(request, 'shop/page4.html', {'categories': categories})


# Функція для сторінки конкретного товару
def product_detail(request, product_id):
    # Шукаємо товар за його ID
    product = get_object_or_404(Product, id=product_id)
    # Беремо всі категорії для бокового меню
    categories = Category.objects.all()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': categories
    })