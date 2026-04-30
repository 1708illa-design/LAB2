from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")

    # --- НОВЕ ПОЛЕ: Вказує, чия це підкатегорія ---
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories',
                               verbose_name="Батьківська категорія")

    def __str__(self):
        # Щоб в адмінці було красиво видно: "Насіння -> Томати"
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

    class Meta:
        verbose_name_plural = "Категорії"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    title = models.CharField(max_length=200, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    # --- ОСЬ ЦЕ НОВЕ ПОЛЕ ДЛЯ ОПИСУ ---
    description = models.TextField(verbose_name="Опис товару", blank=True, null=True)

    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Товари"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    author = models.CharField(max_length=100, verbose_name="Автор відгуку")
    text = models.TextField(verbose_name="Текст")
    # І сюди теж повертаємо:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return f"Відгук від {self.author}"

    class Meta:
        verbose_name_plural = "Відгуки"