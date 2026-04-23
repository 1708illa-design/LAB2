from django.urls import path  # ЦЬОГО РЯДКА У ТЕБЕ НЕ ВИСТАЧАЄ
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('category/<int:category_id>/', views.main_page, name='category_filter'),
    path('page-1/', views.page_one, name='page_1'),
    path('page-2/', views.page_two, name='page_2'),
    path('contacts/', views.page_tree, name='page_3'),
    path('cabinet/', views.page_for, name='page_4'),
]