from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    # auto_now_add запише час при створенні, auto_now - при кожному оновленні
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категорії"

class Product(models.Model):
    # Об'єднуємо таблицю Товари з таблицею Категорії
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    title = models.CharField(max_length=200, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Товари"

class Review(models.Model):
    # Об'єднуємо таблицю Відгуки з таблицею Товари
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    author = models.CharField(max_length=100, verbose_name="Автор відгуку")
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return f"Відгук від {self.author}"

    class Meta:
        verbose_name_plural = "Відгуки"