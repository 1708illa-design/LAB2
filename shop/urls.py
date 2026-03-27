from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('page-1/', views.page_one, name='page_1'),
    path('page-2/', views.page_two, name='page_2'),
]