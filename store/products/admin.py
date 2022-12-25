from django.contrib import admin

from .models import Product, ProductCategory, Basket

# Register your models here.

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = (
        'name',
        'description',
        # вложенный кортеж, позволяет выводить нужные поля на одной строке
        ('price', 'quantity'),
        'image',
        'category'
    )
    # поиск по полю
    search_fields = ('name',)
    ordering = ('category', 'name',)


# модель вставка
# добам ее в модель юсера, и сможем использовать корзину непосредственно принадлежащую автору.
class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    # количество пустых полей, для добавления товара через админку
    extra = 1
