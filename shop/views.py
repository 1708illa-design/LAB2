from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from decimal import Decimal

from .models import Product, Category, Review, Newsletter, Order, OrderItem
from .forms import ReviewForm, NewsletterForm, SignUpForm, OrderForm
from .cart import Cart


# ── ХЕЛПЕР: категорії + newsletter у кожну view ──────────────────
def base_context():
    return {
        'categories': Category.objects.all(),
        'newsletter_form': NewsletterForm(),
    }


# ── ГОЛОВНА ───────────────────────────────────────────────────────
def main_page(request, category_id=None):
    ctx = base_context()
    current_category = None

    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        cats = [current_category] + list(current_category.subcategories.all())
        products_list = Product.objects.filter(category__in=cats).order_by('-created_at')
    else:
        products_list = Product.objects.all().order_by('-created_at')

    paginator = Paginator(products_list, 9)
    products = paginator.get_page(request.GET.get('page'))

    ctx.update({'products': products, 'current_category': current_category})
    return render(request, 'shop/index.html', ctx)


# ── ТОВАР ─────────────────────────────────────────────────────────
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.review_set.all()
    avg_rating = product.get_avg_rating()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, 'Дякуємо за ваш відгук! 🌱')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    ctx = base_context()
    ctx.update({
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
    })
    return render(request, 'shop/product_detail.html', ctx)


# ── РОЗСИЛКА ──────────────────────────────────────────────────────
@require_POST
def subscribe_newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        obj, created = Newsletter.objects.get_or_create(email=form.cleaned_data['email'])
        if created:
            messages.success(request, '✅ Підписку оформлено!')
        else:
            messages.info(request, '📬 Цей email вже підписано.')
    else:
        messages.error(request, '❌ Невірний формат email.')
    return redirect(request.META.get('HTTP_REFERER', 'main'))


# ── КОШИК ─────────────────────────────────────────────────────────
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=int(request.POST.get('quantity', 1)))
    messages.success(request, f'«{product.title}» додано до кошика 🛒')
    return redirect(request.META.get('HTTP_REFERER', 'main'))


@require_POST
def cart_remove(request, product_id):
    Cart(request).remove(get_object_or_404(Product, id=product_id))
    return redirect('cart_detail')


def cart_detail(request):
    ctx = base_context()
    ctx['cart'] = Cart(request)
    ctx['order_form'] = OrderForm()
    return render(request, 'shop/cart_detail.html', ctx)


# ── ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ─────────────────────────────────────────
@login_required
@require_POST
def order_create(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, 'Кошик порожній.')
        return redirect('cart_detail')

    form = OrderForm(request.POST)
    if form.is_valid():
        total = cart.get_total_price()

        order = Order.objects.create(
            user=request.user,
            total_price=total,
            city=form.cleaned_data['city'],
            warehouse=form.cleaned_data['warehouse'],
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
            )

        # Нараховуємо 5% бонусів
        bonus = total * Decimal('0.05')
        profile = request.user.profile
        profile.bonuses += bonus
        profile.save()

        cart.clear()
        messages.success(request, f'🎉 Замовлення №{order.id} оформлено! Нараховано {bonus:.2f} грн бонусів.')
        return redirect('cabinet')

    messages.error(request, 'Перевірте дані доставки.')
    return redirect('cart_detail')


# ── КАБІНЕТ ───────────────────────────────────────────────────────
@login_required
def cabinet(request):
    if request.user.is_staff:
        orders = Order.objects.all().prefetch_related('items__product')
    else:
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')

    ctx = base_context()
    ctx['orders'] = orders
    return render(request, 'shop/cabinet.html', ctx)


# ── АДМІН: зміна статусу ─────────────────────────────────────────
@login_required
@require_POST
def order_change_status(request, order_id):
    if not request.user.is_staff:
        return redirect('cabinet')
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in ['new', 'sent', 'done']:
        order.status = new_status
        order.save()
    return redirect('cabinet')


# ── РЕЄСТРАЦІЯ ────────────────────────────────────────────────────
def signup(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Ласкаво просимо, {user.first_name or user.username}! 🌱')
            return redirect('main')
    else:
        form = SignUpForm()

    ctx = base_context()
    ctx['form'] = form
    return render(request, 'shop/signup.html', ctx)


# ── СТАТИЧНІ СТОРІНКИ ─────────────────────────────────────────────
def page_tree(request):
    return render(request, 'shop/page1.html', base_context())

def page_two(request):
    return render(request, 'shop/page2.html', base_context())

def page_contacts(request):
    return render(request, 'shop/page3.html', base_context())