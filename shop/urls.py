from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('category/<int:category_id>/', views.main_page, name='category_filter'),

    # --- ОСЬ ЦЕЙ РЯДОК МИ ДОДАЛИ ---
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('page-1/', views.page_tree, name='page_1'),
    path('page-2/', views.page_two, name='page_2'),
    path('contacts/', views.page_contacts, name='page_3'),
    path('cabinet/', views.page_cabinet, name='page_4'),
]