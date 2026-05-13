from decimal import Decimal
from .models import Product

CART_SESSION_KEY = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            # Зберігаємо ціну ТІЛЬКИ як рядок для JSON
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        # Отримуємо всі товари з бази одним запитом
        products = Product.objects.filter(id__in=product_ids)
        product_dict = {str(p.id): p for p in products}

        # Копіюємо дані, не псуючи оригінальну сесію
        for product_id, item in self.cart.items():
            # Робимо копію кожного елемента окремо!
            display_item = item.copy()
            display_item['product'] = product_dict.get(product_id)
            display_item['price'] = Decimal(display_item['price'])
            display_item['total_price'] = display_item['price'] * display_item['quantity']
            yield display_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # Розраховуємо суму, завжди перетворюючи рядок у Decimal "на льоту"
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        if CART_SESSION_KEY in self.session:
            del self.session[CART_SESSION_KEY]
            self.save()