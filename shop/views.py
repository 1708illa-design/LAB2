from django.shortcuts import render

def main_page(request):
    # Контекст для головної сторінки
    context = {
        'page_title': 'Головна',
        'is_main': True, # Цей прапорець скаже шаблону показати посилання на інші сторінки
    }
    return render(request, 'index.html', context)

def page_one(request):
    # Контекст для першої сторінки
    context = {
        'page_title': 'Сторінка 1',
        'is_main': False,
        'content': 'Це унікальний контент для першої сторінки.',
    }
    return render(request, 'index.html', context)

def page_two(request):
    # Контекст для другої сторінки
    context = {
        'page_title': 'Сторінка 2',
        'is_main': False,
        'content': 'А це вже текст другої сторінки.',
    }
    return render(request, 'index.html', context)