from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    # (Список EMOJI_CHOICES залишаємо без змін...)
    EMOJI_CHOICES = [
        ('Рослини', (
            ('🌾', '🌾 Колос'), ('🌽', '🌽 Кукурудза'), ('🌻', '🌻 Соняшник'), ('🌱', '🌱 Проросток'),
        )),
        # ... решта категорій
    ]

    name = models.CharField(max_length=28, verbose_name="Назва категорії")
    icon = models.CharField(max_length=10, choices=EMOJI_CHOICES, verbose_name="Іконка (зі списку)", blank=True, null=True)
    custom_icon = models.CharField(max_length=10, verbose_name="АБО вставте свій емоджі", blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name="Батьківська категорія")

    @property
    def final_icon(self):
        return self.custom_icon or self.icon or "🔹"

    def __str__(self):
        return f"{self.parent.name} -> {self.name}" if self.parent else self.name

    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError("Не можна створювати під-під-категорії.")
        if self.parent == self:
            raise ValidationError("Категорія не може бути батьком самої себе.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    title = models.CharField(max_length=100, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    description = models.TextField(verbose_name="Опис товару", blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.title

    def get_avg_rating(self):
        result = self.reviews.aggregate(avg=Avg('rating'))
        return result['avg'] or 0

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")
    author = models.CharField(max_length=100, verbose_name="Автор відгуку")
    text = models.TextField(verbose_name="Текст")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оцінка (1–5)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ['-created_at']

# ЦЕЙ КЛАС МАЄ БУТИ ТУТ!
class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата підписки")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Підписник"
        verbose_name_plural = "Розсилка"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Бонуси")

    def __str__(self):
        return f"Профіль {self.user.username}"

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Order(models.Model):
    STATUS_CHOICES = [('new', 'Нове'), ('sent', 'Відправлено'), ('done', 'Виконано')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупець")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    city = models.CharField(max_length=100, verbose_name="Місто")
    warehouse = models.CharField(max_length=200, verbose_name="Відділення")

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Замовлення")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    class Meta:
        verbose_name = "Товар у замовленні"
        verbose_name_plural = "Товари в замовленнях"