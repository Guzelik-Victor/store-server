from django.contrib import admin

from .models import Basket, Product, ProductCategory, Image

# Register your models here.

admin.site.register(ProductCategory)


class ImageInline(admin.TabularInline):
    model = Image
    fields = ('product', 'image')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = (
        'name',
        'description',
        # вложенный кортеж, позволяет выводить нужные поля на одной строке
        ('price', 'quantity'),
        'stripe_product_price_id',
        'category'
    )
    # поиск по полю
    search_fields = ('name',)
    ordering = ('category', 'name',)
    inlines = (ImageInline,)



# модель вставка
# добавим ее в модель юзера, и сможем использовать корзину непосредственно принадлежащую автору.
class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    # количество пустых полей, для добавления товара через админку
    extra = 1
