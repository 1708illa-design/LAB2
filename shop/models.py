from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    # Твій мега-список емодзі
    EMOJI_CHOICES = [
        ('Рослини', (
            ('🌾', '🌾 Колос'), ('🌽', '🌽 Кукурудза'), ('🌻', '🌻 Соняшник'), ('🌱', '🌱 Проросток'),
            ('🌿', '🌿 Трава'), ('🥜', '🥜 Арахіс'), ('🎋', '🎋 Бамбук'), ('🎍', '🎍 Декор'),
            ('🍀', '🍀 Конюшина'), ('☘️', '☘️ Трилисник'), ('🍂', '🍂 Листя'), ('🍁', '🍁 Клен'),
            ('🌵', '🌵 Кактус'), ('🌴', '🌴 Пальма'), ('🌳', '🌳 Дерево'), ('🌲', '🌲 Ялина'),
            ('🪵', '🪵 Дрова'), ('🍄', '🍄 Гриб'), ('🍃', '🍃 Зелень'), ('🪴', '🪴 Вазон'),
            ('🏵️', '🏵️ Квітка'), ('🌹', '🌹 Роза'), ('🌸', '🌸 Сакура'), ('💐', '💐 Букет'),
            ('🌼', '🌼 Ромашка'), ('🌷', '🌷 Тюльпан'), ('🥀', '🥀 Троянда'), ('🌺', '🌺 Гібіскус'),
            ('💮', '💮 Вишня'),
        )),
        ('Овочі та Фрукти', (
            ('🍏', '🍏 Яблуко зелене'), ('🍎', '🍎 Яблуко червоне'), ('🍐', '🍐 Груша'), ('🍊', '🍊 Мандарин'),
            ('🍋', '🍋 Лимон'), ('🍌', '🍌 Банан'), ('🍉', '🍉 Кавун'), ('🍇', '🍇 Виноград'),
            ('🍓', '🍓 Полуниця'), ('🫐', '🫐 Лохина'), ('🍈', '🍈 Диня'), ('🍒', '🍒 Вишня'),
            ('🍑', '🍑 Персик'), ('🥭', '🥭 Манго'), ('🍍', '🍍 Ананас'), ('🥥', '🥥 Кокос'),
            ('🥝', '🥝 Ківі'), ('🍅', '🍅 Томат'), ('🥒', '🥒 Огірок'), ('🍆', '🍆 Баклажан'),
            ('🫑', '🫑 Перець'), ('🌶️', '🌶️ Чилі'), ('🎃', '🎃 Гарбуз'), ('🥕', '🥕 Морква'),
            ('🥔', '🥔 Картопля'), ('🧅', '🧅 Цибуля'), ('🧄', '🧄 Часник'), ('🍠', '🍠 Батат'),
            ('🥦', '🥦 Брокколі'), ('🥬', '🥬 Салат'), ('🥗', '🥗 Зелень'), ('🫛', '🫛 Горох'),
            ('🫘', '🫘 Квасоля'),
        )),
        ('Хімія та Захист', (
            ('🧪', '🧪 Колба'), ('⚗️', '⚗️ Дистилят'), ('🧬', '🧬 ДНК'), ('💎', '💎 Кристал'),
            ('💊', '💊 Таблетки'), ('💧', '💧 Крапля'), ('🔋', '🔋 Енергія'), ('🛡️', '🛡️ Захист'),
            ('⚔️', '⚔️ Гербіцид'), ('🦠', '🦠 Бактерія'), ('🚫', '🚫 Заборона'), ('🌫️', '🌫️ Туман'),
            ('🧼', '🧼 Прилипач'), ('🔬', '🔬 Мікроскоп'), ('🩹', '🩹 Пластир'), ('💉', '💉 Ін’єкція'),
            ('🌡️', '🌡️ Температура'),
        )),
        ('Техніка та Інструмент', (
            ('🚜', '🚜 Трактор'), ('✂️', '✂️ Секатор'), ('🪚', '🪚 Пила'), ('🧤', '🧤 Рукавички'),
            ('🧺', '🧺 Кошик'), ('⚙️', '⚙️ Шестерня'), ('🪝', '🪝 Гак'), ('🧹', '🧹 Мітла'),
            ('🔨', '🔨 Молоток'), ('⚒️', '⚒️ Кайло'), ('⛏️', '⛏️ Кирка'), ('🔧', '🔧 Ключ'),
            ('🔩', '🔩 Гвинт'), ('🛒', '🛒 Візок'), ('📦', '📦 Коробка'), ('🏷️', '🏷️ Бірка'),
            ('🚚', '🚚 Вантажівка'), ('🚛', '🚛 Фура'), ('🚲', '🚲 Велосипед'), ('🏍️', '🏍️ Мотоблок'),
        )),
        ('Полив та Будинки', (
            ('🚿', '🚿 Полив'), ('⛲', '⛲ Фонтан'), ('🌀', '🌀 Шланг'), ('🚰', '🚰 Кран'),
            ('🏺', '🏺 Горщик'), ('🏠', '🏠 Будинок'), ('🛖', '🛖 Теплиця'), ('🏘️', '🏘️ Склад'),
            ('🏗️', '🏗️ Будівництво'), ('🏭', '🏭 Завод'),
        )),
        ('Агроволокно та Покриття', (
            ('🧵', '🧵 Агроволокно (загальне)'),
            ('🌫️', '🌫️ Біле (укривне)'),
            ('⬛', '⬛ Чорне (мульчувальне)'),
            ('🕸️', '🕸️ Сітка шпалерна'),
            ('🏁', '🏁 Затіняюча сітка'),
            ('🏠', '🏠 Плівка для теплиць'),
            ('🏳️', '🏳️ Агротканина'),
        )),
    ]

    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    icon = models.CharField(
        max_length=10,
        choices=EMOJI_CHOICES,
        verbose_name="Іконка (emoji)",
        blank=True,
        default="🔹"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Батьківська категорія"
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError("Не можна створювати під-під-категорії.")
        if self.parent == self:
            raise ValidationError("Категорія не може бути батьком самої себе.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Категорії"

# --- ОСЬ ЦІ МОДЕЛІ МАЮТЬ ПОВЕРНУТИСЯ ---
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    title = models.CharField(max_length=200, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return f"Відгук від {self.author}"

    class Meta:
        verbose_name_plural = "Відгуки"