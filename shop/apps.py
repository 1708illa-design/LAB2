from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        """Цей метод викликається один раз при запуску Django.
        Він імпортує файл сигналів, щоб вони почали 'слухати' події."""
        import shop.signals