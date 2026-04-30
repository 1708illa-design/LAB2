from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator

def main_page(request, category_id=None):
    # Отримуємо всі категорії для бокового меню
    categories = Category.objects.all()
    current_category = None

    # Фільтрація за категорією (Логіка Лаби №6)
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        products_list = Product.objects.filter(category=current_category)
    else:
        products_list = Product.objects.all()

    # Пагінація (залишив 9 товарів, як у тебе було)
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category, # Тепер шаблон знатиме, яка категорія обрана
    })

# Функції для статичних сторінок (Як замовити, Доставка тощо)
def page_tree(request): # Твоя функція для page1.html
    categories = Category.objects.all()
    return render(request, 'shop/page1.html', {'categories': categories})

def page_two(request): # Твоя функція для page2.html
    categories = Category.objects.all()
    return render(request, 'shop/page2.html', {'categories': categories})

def page_contacts(request): # Твоя функція для сторінки контактів (page3)
    categories = Category.objects.all()
    return render(request, 'shop/page3.html', {'categories': categories})

def page_cabinet(request): # Твоя функція для кабінету (page4)
    categories = Category.objects.all()
    return render(request, 'shop/page4.html', {'categories': categories})