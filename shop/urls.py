from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ── ГОЛОВНА ТА КАТЕГОРІЇ ─────────────────────────────────────
    path('', views.main_page, name='main'),
    path('category/<int:category_id>/', views.main_page, name='category_filter'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # ── РОЗСИЛКА ─────────────────────────────────────────────────
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # ── КОШИК ────────────────────────────────────────────────────
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),

    # ── ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ────────────────────────────────────
    path('checkout/', views.checkout, name='checkout'),

    # ── КАБІНЕТ ТА ЗАМОВЛЕННЯ ────────────────────────────────────
    path('cabinet/', views.cabinet, name='cabinet'),
    path('order/<int:order_id>/status/', views.order_change_status, name='order_change_status'),

    # ── РЕЄСТРАЦІЯ ТА ВХІД ───────────────────────────────────────
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),

    # ── ВІДНОВЛЕННЯ ПАРОЛЯ ───────────────────────────────────────
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='shop/password_reset.html',
        email_template_name='shop/password_reset_email.html',
        subject_template_name='shop/password_reset_subject.txt',
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='shop/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='shop/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='shop/password_reset_complete.html'
    ), name='password_reset_complete'),

    # ── СТАТИЧНІ СТОРІНКИ ────────────────────────────────────────
    path('page-1/', views.page_tree, name='page_1'),
    path('page-2/', views.page_two, name='page_two'),
    path('contacts/', views.page_contacts, name='contacts'),
]