from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator


def main_page(request, category_id=None):
    categories = Category.objects.all()

    # Фільтрація
    if category_id:
        products_list = Product.objects.filter(category_id=category_id)
    else:
        products_list = Product.objects.all()

    # Пагінація (по 4 товари)
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories,
    })


# Обов'язково додаємо ці функції, щоб не було помилок
def page_one(request):
    categories = Category.objects.all()
    return render(request, 'shop/page1.html', {'categories': categories})


def page_two(request):
    categories = Category.objects.all()
    return render(request, 'shop/page2.html', {'categories': categories})
def page_tree(request):
    categories = Category.objects.all()
    return render(request, 'shop/page3.html', {'categories': categories})

def page_for(request):
    categories = Category.objects.all()
    return render(request, 'shop/page4.html', {'categories': categories})