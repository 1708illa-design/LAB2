from django.contrib import admin
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import (
    Category, Product, Review, Newsletter, NewsletterCampaign,
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


# --- ПІДПИСНИКИ (ОНОВЛЕНО) ---
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_active',)
    readonly_fields = ('created_at',)


# --- МАСОВА РОЗСИЛКА (НОВЕ) ---
@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'sent')
    readonly_fields = ('sent', 'created_at')

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # Перевіряємо, чи це нова розсилка, а не редагування старої
        super().save_model(request, obj, form, change)

        # Якщо ми щойно створили нову розсилку — відправляємо листи!
        if is_new and not obj.sent:
            # Беремо всі пошти активних підписників
            subscribers = Newsletter.objects.filter(is_active=True).values_list('email', flat=True)

            if subscribers:
                # Офіційний шаблон для листів
                official_message = f"""Вітаємо! Це офіційне повідомлення від магазину AGRIS 🌱

{obj.message}

---
З повагою,
Ваш надійний партнер — Агромагазин AGRIS.
📞 0 (99) 646-18-61
📍 м. Луцьк, вул. Соборності, 14

Ви отримали цей лист, оскільки підписані на нашу розсилку.
"""
                # Формуємо пачку листів
                messages = tuple(
                    (obj.subject, official_message, settings.DEFAULT_FROM_EMAIL, [email])
                    for email in subscribers
                )

                try:
                    send_mass_mail(messages, fail_silently=False)
                    # Відмічаємо, що розсилка успішно відправлена
                    obj.sent = True
                    obj.save()
                except Exception as e:
                    print(f"Помилка масової розсилки: {e}")


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