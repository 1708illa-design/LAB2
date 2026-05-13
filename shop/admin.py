from django.contrib import admin
from .models import (
    Category, Product, Review, Newsletter,
    Profile, Order, OrderItem, SiteConfiguration
)


# --- НАЛАШТУВАННЯ САЙТУ (ФОН АВТОРИЗАЦІЇ) ---
@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'auth_background')

    def has_add_permission(self, request):
        # Якщо вже є хоча б один запис, кнопка "Додати" зникне
        if SiteConfiguration.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Забороняємо видаляти останній запис, щоб налаштування завжди були
        return False


# --- ВІДОБРАЖЕННЯ ТОВАРІВ ВСЕРЕДИНІ ЗАМОВЛЕННЯ (Inline) ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)


# --- КАТЕГОРІЇ ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'final_icon', 'name', 'parent')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# --- ТОВАРИ ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('category',)


# --- ВІДГУКИ ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'product')
    search_fields = ('author', 'text')
    readonly_fields = ('created_at',)


# --- ПІДПИСНИКИ ---
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)


# --- ПРОФІЛІ ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'bonuses')
    search_fields = ('user__username', 'phone')


# --- ЗАМОВЛЕННЯ ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'city', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('user__username', 'city')
    inlines = [OrderItemInline]


# --- ПОЗИЦІЇ ЗАМОВЛЕННЯ ---
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')