from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from products.models import Basket, Product, ProductCategory
from users.models import User


class IndexViewTestCase(TestCase):

    def test_index(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ('categories.json', 'goods.json',)

    def setUp(self):
        self.products = Product.objects.all()
        self.categories = ProductCategory.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products[:3])
        )

    def test_list_with_category(self):
        category = self.categories.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id)[:3])
        )

    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')


class BasketAddTestCase(TestCase):
    fixtures = ('categories.json', 'goods.json',)

    def setUp(self):
        self.products = Product.objects.all()
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client(
            HTTP_REFERER='http://127.0.0.1:8000/products/'
        )
        self.authorized_client.force_login(self.user)

    def test_not_authorized_client_add_basket(self):
        product = self.products.first()
        path = reverse('products:basket_add', kwargs={'product_id': product.id})
        response = self.guest_client.get(path, follow=True)
        self.assertRedirects(
            response, '/users/login/?next=/products/baskets/add/1/'
        )

    def test_authorized_client_add_basket(self):
        product = self.products.first()
        self.assertFalse(
            Basket.objects.filter(
                user=self.user,
                product=product
            ).exists()
        )
        path = reverse('products:basket_add', kwargs={'product_id': product.id})
        self.authorized_client.get(path, follow=True)
        self.assertTrue(
            Basket.objects.filter(
                user=self.user,
                product=product
            ).exists()
        )


class BasketRemoveTestCase(TestCase):
    fixtures = ('categories.json', 'goods.json',)

    def setUp(self):
        self.products = Product.objects.all()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client(
            HTTP_REFERER='http://127.0.0.1:8000/products/'
        )
        self.authorized_client.force_login(self.user)
        self.product = self.products.first()
        self.basket = Basket.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

    def test_authorized_client_remove_basket(self):
        self.assertTrue(
            Basket.objects.filter(
                user=self.user,
                product=self.product
            ).exists()
        )
        self.assertEqual(Basket.objects.total_quantity(), 1)

        path = reverse(
            'products:basket_remove',
            kwargs={'basket_id': self.basket.id}
        )

        self.authorized_client.get(path, follow=True)

        self.assertFalse(
            Basket.objects.filter(
                user=self.user,
                product=self.product
            ).exists()
        )
        self.assertEqual(Basket.objects.total_quantity(), 0)


class PaginatorViewsTest(TestCase):
    fixtures = ('categories.json', 'goods.json',)
    product_per_page = 3

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_products(self):
        response = self.client.get(
            reverse('products:paginator', kwargs={'page': 1})
        )
        self.assertEqual(
            len(response.context['object_list']),
            self.product_per_page
        )

    def test_second_page_products(self):
        response = self.client.get(
            reverse('products:paginator', kwargs={'page': 2})
        )
        self.assertEqual(
            len(response.context['object_list']),
            self.product_per_page
        )
