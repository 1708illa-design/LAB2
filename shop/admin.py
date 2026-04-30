from django.contrib import admin
from .models import Category, Product

# Налаштування для Категорій
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Залишаємо тільки ті поля, які реально є в моделі Category
    list_display = ('id', 'name', 'parent')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

# Налаштування для Товарів (тут created_at і updated_at можна залишити, бо вони є в моделі Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('category', 'price')