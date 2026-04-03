from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Вимога: видно назву, створено о, оновлено о
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Додав ще категорію та ціну, щоб було зрозуміло, що це за товар
    list_display = ('title', 'category', 'price', 'created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'created_at', 'updated_at')