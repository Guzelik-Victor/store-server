
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.urls import reverse

from .common.views import TitleMixin
from .models import Basket, Product, ProductCategory, Image


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - {self.object.name}'
        image = cache.get(f'image {self.object.id}')
        if not image:
            context['image'] = Image.objects.filter(product_id=self.object.id)
            cache.set(f'image {self.object.id}', context['image'], 30)
        else:
            context['image'] = image
        return context


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 6
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        queryset = queryset.prefetch_related('image')
        category_id = self.kwargs.get('category_id')
        return (
            queryset.filter(category_id=category_id)
            if category_id else queryset
        )

# пример реализация кэша во вью
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 20)
        else:
            context['categories'] = categories
        return context


@login_required
def basket_add(request, product_id):

    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    quantity = int(request.POST['quantity'])

    # найти вариант решения (может полноценно через модел форм)
    # форма для валидации
    #form = QuantityForm(request.POST)
    #form.data = form.data.copy()
    #form.data['product_id'] = int(product.id)

    #form.data._mutable = True
    #form.data['product_id'] = product.id
    #form.data._mutable = False
    # if form.is_valid():
    if not baskets.exists():
        Basket.objects.create(
            user=request.user,
            product=product,
            quantity=quantity
        )
    else:
        basket = baskets.first()
        if basket.quantity + quantity <= product.quantity:
            basket.quantity += quantity
            basket.save()
        else:
            messages.info(
                request,
                f'Недопустимое количество товара.<br>'
                f'В корзине {basket.quantity} ед. указанного товара.<br>'
                f'Всего товара на складе: {product.quantity} ед.<br>'
                f'Можно добавить {product.quantity-basket.quantity} ед.'

            )
            return redirect(
                reverse('products:product_detail', kwargs={'pk': product.id})
            )
    return redirect(request.META['HTTP_REFERER'])


@login_required
def basket_update(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = get_object_or_404(Basket, user=request.user, product=product)
    quantity = request.POST['quantity']
    if not quantity:
        basket.delete()
    else:
        basket.quantity = int(quantity)
        basket.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])
