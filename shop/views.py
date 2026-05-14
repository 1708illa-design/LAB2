from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal

from .models import Product, Category, Review, Newsletter, Order, OrderItem, Profile
from .forms import ReviewForm, NewsletterForm, SignUpForm, OrderForm, ProfileForm
from .cart import Cart


def base_context():
    """Базовий контекст, що повторюється на всіх сторінках."""
    return {
        'categories': Category.objects.filter(parent=None).prefetch_related('subcategories'),
        'newsletter_form': NewsletterForm(),
    }


def main_page(request, category_id=None):
    ctx = base_context()
    current_category = None

    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        # Отримуємо продукти поточної категорії та всіх її підкатегорій
        cats = [current_category] + list(current_category.subcategories.all())
        products_list = Product.objects.filter(category__in=cats).order_by('-created_at')
    else:
        products_list = Product.objects.all().order_by('-created_at')

    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    ctx.update({
        'products': products,
        'current_category': current_category
    })
    return render(request, 'shop/index.html', ctx)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Увійдіть, щоб залишити відгук.')
            return redirect('login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Відгук додано! 🌱')
            return redirect('product_detail', product_id=product.id)

    ctx = base_context()
    ctx.update({
        'product': product,
        'reviews': product.reviews.all().order_by('-created_at'),
        'form': ReviewForm()
    })
    return render(request, 'shop/product_detail.html', ctx)


# ─── РОЗСИЛКА (З ВІТАЛЬНИМ ЛИСТОМ) ───────────────────────────────────────
@require_POST
def subscribe_newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        obj, created = Newsletter.objects.get_or_create(email=email)

        if created:
            # === ОФІЦІЙНИЙ ПРИВІТАЛЬНИЙ ЛИСТ ===
            subject = '🌱 Вітаємо в родині AGRIS! Підписка успішна'
            message = f"""Вітаємо!

Ви успішно прив'язали свою пошту {email} до нашої системи.

Дякуємо, що погодилися отримувати наші новини. Тепер ви першими дізнаватиметесь про:
🌾 Свіжі надходження насіння
🔥 Секретні акції та знижки
📚 Корисні поради для вашого саду та городу

---
З повагою,
Команда офіційного агромагазину AGRIS.
м. Луцьк, вул. Соборності, 14
"""
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                messages.success(request, '✅ Підписку оформлено! Ми надіслали вам привітального листа.')
            except Exception:
                messages.success(request, '✅ Підписку оформлено! (Лист не відправлено через локальні налаштування)')
        else:
            # Якщо людина відписувалась, а тепер знову підписалась
            if not obj.is_active:
                obj.is_active = True
                obj.save()
                messages.success(request, '✅ Вашу підписку відновлено!')
            else:
                messages.info(request, '📬 Цей email вже підписано.')

    return redirect(request.META.get('HTTP_REFERER', 'main'))


# ─── КОШИК (З ПІДТРИМКОЮ AJAX) ───────────────────────────────────────
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)

    # 🟢 ПЕРЕВІРКА НА AJAX ЗАПИТ
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'cart_length': len(cart),
            'product_title': product.title
        })

    messages.success(request, f'"{product.title}" додано у кошик! 🛒')
    return redirect(request.META.get('HTTP_REFERER', 'main'))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect('cart_detail')


def cart_detail(request):
    ctx = base_context()
    ctx['cart'] = Cart(request)
    return render(request, 'shop/cart_detail.html', ctx)


# ─── ЧЕКАУТ (З БОНУСАМИ) ─────────────────────────────────────────────
@login_required
@transaction.atomic
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Ваш кошик порожній.")
        return redirect('cart_detail')

    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total = cart.get_total_price()

            # ЛОГІКА СПИСАННЯ БОНУСІВ
            if form.cleaned_data.get('use_bonuses') and profile.bonuses > 0:
                if profile.bonuses >= total:
                    profile.bonuses -= total
                    total = Decimal('0.00')
                else:
                    total -= profile.bonuses
                    profile.bonuses = Decimal('0.00')
                profile.save()

            # Створення замовлення
            order = Order.objects.create(
                user=request.user,
                total_price=total,
                last_name=form.cleaned_data['last_name'],
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data.get('middle_name', ''),
                phone=form.cleaned_data['phone'],
                city=request.POST.get('city', ''),
                warehouse=request.POST.get('warehouse', '')
            )

            # Перенесення товарів з кошика в замовлення
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            # Оновлення профілю для майбутніх автозаповнень
            profile.phone = form.cleaned_data['phone']
            profile.last_name = form.cleaned_data['last_name']
            profile.first_name = form.cleaned_data['first_name']
            profile.save()

            cart.clear()
            messages.success(request, f'🎉 Замовлення №{order.id} успішно оформлено!')
            return redirect('cabinet')
    else:
        # Предзаповнення форми даними профілю
        initial_data = {
            'last_name': profile.last_name or request.user.last_name,
            'first_name': profile.first_name or request.user.first_name,
            'middle_name': profile.middle_name,
            'phone': profile.phone,
        }
        form = OrderForm(initial=initial_data)

    ctx = base_context()
    ctx.update({'cart': cart, 'order_form': form, 'profile': profile})
    return render(request, 'shop/checkout.html', ctx)


# ─── КАБІНЕТ (ФІЛЬТРАЦІЯ ТА ПАГІНАЦІЯ) ────────────────────────
@login_required
def cabinet(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Ваші дані збережено!')
            return redirect('cabinet')
    else:
        profile_form = ProfileForm(instance=profile)

    status_filter = request.GET.get('status')

    if request.user.is_staff:
        orders_list = Order.objects.all().prefetch_related('items__product')
    else:
        orders_list = Order.objects.filter(user=request.user).prefetch_related('items__product')

    if status_filter in ['new', 'sent', 'done']:
        orders_list = orders_list.filter(status=status_filter)

    orders_list = orders_list.order_by('-created_at')

    paginator = Paginator(orders_list, 5)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    ctx = base_context()
    ctx.update({
        'orders': orders,
        'profile': profile,
        'profile_form': profile_form,
        'current_status_filter': status_filter
    })
    return render(request, 'shop/cabinet.html', ctx)


@login_required
@require_POST
def order_change_status(request, order_id):
    """Зміна статусу (тільки стафф) + автоматичне нарахування бонусів."""
    if not request.user.is_staff:
        return redirect('main')

    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')

    # Перевіряємо, чи саме в цей момент статус змінюється на "done"
    just_awarded = (new_status == 'done' and not order.bonuses_awarded)

    order.status = new_status
    # ВИКЛИК .save() АВТОМАТИЧНО НАРАХУЄ БОНУСИ ЧЕРЕЗ models.py!
    order.save()

    if just_awarded:
        earned_bonus = order.total_price * Decimal('0.05')
        messages.success(request, f'Замовлення №{order.id} виконано! Клієнту нараховано кешбек: {earned_bonus:.2f} ₴ 🎁')
    else:
        messages.success(request, f'Статус замовлення №{order.id} успішно змінено.')

    return redirect(request.META.get('HTTP_REFERER', 'cabinet'))


# ─── РЕЄСТРАЦІЯ ТА СТАТИЧНІ СТОРІНКИ ──────────────────────────────────
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ЯВНЕ І БЕЗПЕЧНЕ СТВОРЕННЯ ПРОФІЛЮ
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('signup_success')
    else:
        form = SignUpForm()

    ctx = base_context()
    ctx['form'] = form
    return render(request, 'shop/signup.html', ctx)


def signup_success(request):
    return render(request, 'shop/signup_success.html', base_context())


def page_tree(request):
    return render(request, 'shop/page1.html', base_context())


def page_two(request):
    return render(request, 'shop/page2.html', base_context())


def page_contacts(request):
    return render(request, 'shop/page3.html', base_context())
