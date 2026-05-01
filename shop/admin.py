
from django.contrib import admin
from .models import Category, Product, Review  # <--- Додали Review сюди
# Реєструємо КАТЕГОРІЇ (тільки один раз!)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Додаємо icon, щоб було видно смайлики прямо у списку
    list_display = ('id', 'icon', 'name', 'parent')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

    # Наше обмеження, щоб не створювати під-під-категорії
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Реєструємо ТОВАРИ
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('category', 'price')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Які колонки показувати в списку відгуків
    list_display = ('author', 'product', 'created_at')

    # Фільтри збоку (дуже зручно шукати відгуки за датою або товаром)
    list_filter = ('created_at', 'product')

    # Поле пошуку (можна шукати по імені автора або тексту відгуку)
    search_fields = ('author', 'text')

    # Тільки для читання (щоб випадково не змінити дату створення)
    readonly_fields = ('created_at', 'updated_at')