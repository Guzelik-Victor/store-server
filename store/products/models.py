import stripe
from _decimal import Decimal
from django.conf import settings
from django.db import models

from users.models import User


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField('Наименование', max_length=128, unique=True)
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField('Наименование', max_length=256)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=0)
    stripe_product_price_id = models.CharField(
        max_length=128, null=True, blank=True
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='category',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('-quantity',)

    def __str__(self) -> str:
        return f'Продукт: {self.name} | Категория: {self.category.name}'

    # Перед сохранением добавляем новый продукт в бд stripe и заполняем наше
    # поле с id от stripe
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(
            force_insert=False, force_update=False, using=None,
            update_fields=None)

    # для онлайн оплаты, через пакет страйп создаем id продукта
    # его цену в бд stripe.
    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='rub'
        )
        return stripe_product_price


class Image(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='image'
    )
    image = models.ImageField('Изображение', upload_to='products_images')

    def __str__(self) -> str:
        return f'Изображение товара: {self.product.name}'


# расширяем метод QuerySet, добавляя к его методам нужные нам
class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        # self - это QuerySet к которму мы будем применять метод
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='товар'
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        default=0,)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    # переопределяем менеджер для обращений к классу баскет
    # теперь нам доступны методы все методы
    # QuerySet плюс total_sum и total_quantity
    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['created_timestamp']

    def __str__(self) -> str:
        return f'Корзина: {self.user.username} | Продукт: {self.product.name}'

    def sum(self) -> Decimal:
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item
