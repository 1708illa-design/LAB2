from django.contrib import admin
from django.urls import path, include # Додай include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')), # Підключаємо маршрути з shop
]