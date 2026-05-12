from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Головна та категорії
    path('', views.main_page, name='main'),
    path('category/<int:category_id>/', views.main_page, name='category_filter'),

    # Сторінка товару
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Розсилка
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # Кошик
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # Оформлення замовлення та кабінет
    path('order/create/', views.order_create, name='order_create'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('order/<int:order_id>/status/', views.order_change_status, name='order_change_status'),

    # Авторизація та Реєстрація (Лаба 3)
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Статичні сторінки (Лаба 3)
    path('page-1/', views.page_tree, name='page_1'),
    path('page-2/', views.page_two, name='page_2'),
    path('contacts/', views.page_contacts, name='contacts'),
]