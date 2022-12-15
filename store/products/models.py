from django.db import models

from users.models import User


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
    price = models.DecimalField('Цена', max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=0)
    image = models.ImageField('Изображение', upload_to='products_images')
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='category',
        verbose_name='Категория'
    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return f'Продукт: {self.name} | Категория: {self.category.name}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


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
    quantity = models.PositiveSmallIntegerField('Количество', default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self) -> str:
        return f'Корзина: {self.user.username} | Продукт: {self.product.name}'

    def sum(self) -> float:
        return self.product.price * self.quantity
