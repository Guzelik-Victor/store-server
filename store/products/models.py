from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('Наименование', max_length=128, unique=True)
    description = models.TextField('Описание', null=True, blank=True)

    class meta:
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
    
    class meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return f'Продукт: {self.name} | Категория: {self.category.name}'
