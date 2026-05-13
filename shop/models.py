from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.contrib.auth.models import User
from decimal import Decimal


# --- ГЛОБАЛЬНІ НАЛАШТУВАННЯ САЙТУ ---
class SiteConfiguration(models.Model):
    auth_background = models.ImageField(
        upload_to='settings/',
        verbose_name="Фон сторінок авторизації",
        help_text="Зображення, яке буде фоном на сторінках входу/реєстрації",
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self):
        return "Налаштування сайту"


# --- КАТЕГОРІЇ ---
class Category(models.Model):
    EMOJI_CHOICES = [
        ('Рослини та Квіти', (
            ('🌾', '🌾 Колос'), ('🌽', '🌽 Кукурудза'), ('🌻', '🌻 Соняшник'), ('🌱', '🌱 Проросток'),
            ('🌿', '🌿 Трава'), ('🥜', '🥜 Арахіс'), ('🎋', '🎋 Бамбук'), ('🎍', '🎍 Декор'),
            ('🍀', '🍀 Конюшина'), ('☘️', '☘️ Трилисник'), ('🍂', '🍂 Листя'), ('🍁', '🍁 Клен'),
            ('🌵', '🌵 Кактус'), ('🌴', '🌴 Пальма'), ('🌳', '🌳 Дерево'), ('🌲', '🌲 Ялина'),
            ('🪵', '🪵 Дрова'), ('🍄', '🍄 Гриб'), ('🍃', '🍃 Зелень'), ('🪴', '🪴 Вазон'),
            ('🏵️', '🏵️ Квітка'), ('🌹', '🌹 Роза'), ('🌸', '🌸 Сакура'), ('💐', '💐 Букет'),
            ('🌼', '🌼 Ромашка'), ('🌷', '🌷 Тюльпан'), ('🥀', '🥀 Троянда'), ('🌺', '🌺 Гібіскус'),
            ('💮', '💮 Вишня'), ('🎈', '🎈 Декор'), ('✨', '✨ Елітне'),
        )),
        ('Овочі, Фрукти, Ягоди', (
            ('🍏', '🍏 Яблуко зелене'), ('🍎', '🍎 Яблуко червоне'), ('🍐', '🍐 Груша'), ('🍊', '🍊 Мандарин'),
            ('🍋', '🍋 Лимон'), ('🍌', '🍌 Банан'), ('🍉', '🍉 Кавун'), ('🍇', '🍇 Виноград'),
            ('🍓', '🍓 Полуниця'), ('🫐', '🫐 Лохина'), ('🍈', '🍈 Диня'), ('🍒', '🍒 Вишня'),
            ('🍑', '🍑 Персик'), ('🥭', '🥭 Манго'), ('🍍', '🍍 Ананас'), ('🥥', '🥥 Кокос'),
            ('🥝', '🥝 Ківі'), ('🍅', '🍅 Томат'), ('🥒', '🥒 Огірок'), ('🍆', '🍆 Баклажан'),
            ('🫑', '🫑 Перець'), ('🌶️', '🌶️ Чилі'), ('🎃', '🎃 Гарбуз'), ('🥕', '🥕 Морква'),
            ('🥔', '🥔 Картопля'), ('🧅', '🧅 Цибуля'), ('🧄', '🧄 Часник'), ('🍠', '🍠 Батат'),
            ('🥦', '🥦 Брокколі'), ('🥬', '🥬 Салат'), ('🥗', '🥗 Зелень'), ('🫛', '🫛 Горох'),
            ('🫘', '🫘 Квасоля'), ('🌽', '🌽 Зерно'),
        )),
    ]

    name = models.CharField(max_length=24, verbose_name="Назва категорії")
    icon = models.CharField(max_length=10, choices=EMOJI_CHOICES, verbose_name="Іконка (зі списку)", blank=True,
                            null=True)
    custom_icon = models.CharField(max_length=10, verbose_name="АБО свій емоджі", blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories',
                               verbose_name="Батьківська категорія")

    @property
    def final_icon(self):
        return self.custom_icon or self.icon or "🔹"

    def __str__(self):
        return f"{self.parent.name} -> {self.name}" if self.parent else self.name

    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError("Не можна створювати під-під-категорії. Дозволено лише один рівень вкладеності.")
        if self.parent == self:
            raise ValidationError("Категорія не може бути батьківською для самої себе.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


# --- ТОВАРИ ---
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
        return round(result['avg'], 1) if result['avg'] else 0

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


# --- ПРОФІЛЬ КОРИСТУВАЧА ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Бонуси")

    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Прізвище")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="По батькові")

    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Місто")
    warehouse = models.CharField(max_length=255, blank=True, null=True, verbose_name="Відділення НП")
    index = models.CharField(max_length=20, blank=True, null=True, verbose_name="Індекс")

    def __str__(self):
        return f"Профіль: {self.user.username}"


# --- ЗАМОВЛЕННЯ ---
class Order(models.Model):
    STATUS_CHOICES = [('new', 'Нове'), ('sent', 'Відправлено'), ('done', 'Виконано')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")

    # === ОСЬ ЦЕ ПОЛЕ ВИРІШУЄ ПРОБЛЕМУ З ЧЕКАУТОМ ===
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="По батькові")

    phone = models.CharField(max_length=20, verbose_name="Телефон")
    city = models.CharField(max_length=100, verbose_name="Місто/Село")
    warehouse = models.CharField(max_length=255, verbose_name="Відділення")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Загальна сума")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    bonuses_awarded = models.BooleanField(default=False, verbose_name="Бонуси нараховано")

    def save(self, *args, **kwargs):
        # Нарахування бонусів при зміні статусу на 'done'
        if self.status == 'done' and not self.bonuses_awarded:
            bonus_amount = self.total_price * Decimal('0.05')  # 5% кешбеку
            self.user.profile.bonuses += bonus_amount
            self.user.profile.save()
            self.bonuses_awarded = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"


# --- ТОВАРИ У ЗАМОВЛЕННІ ---
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Замовлення")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна продажу")

    def get_total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "Товар у замовленні"
        verbose_name_plural = "Товари у замовленні"


# --- ВІДГУКИ ТА РОЗСИЛКА ---
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Користувач")
    author = models.CharField(max_length=100, verbose_name="Автор відгуку")
    text = models.TextField(verbose_name="Текст")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                              verbose_name="Оцінка (1–5)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата підписки")