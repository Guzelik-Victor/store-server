from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .serializers import ProductSerializer, BasketSerializer
from products.models import Product, Basket


class ProductRetrieveListApiView(ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related(
        'images')
    serializer_class = ProductSerializer


class BasketsViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(BasketsViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            quantity = float(request.data['quantity'])
            product = Product.objects.filter(id=product_id)
            if not product.exists():
                return Response(
                    {'product_id': 'Продукты с таким ID не существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            product = product.first()
            if product.quantity < quantity:
                return Response(
                    {
                        'quantity':
                            f'Максимальное количество товара'
                            f'{product.quantity}.'
                     },
                    status=status.HTTP_400_BAD_REQUEST
                )
            baskets = Basket.objects.filter(
                user=request.user, product=product.id
            )
            if not baskets.exists():
                obj = Basket.objects.create(
                    user=request.user,
                    product=product,
                    quantity=quantity
                )
                serializer = self.get_serializer(obj)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            else:
                basket = baskets.first()
                if basket.quantity + quantity <= product.quantity:
                    basket.quantity += quantity
                    basket.save()
                    serializer = self.get_serializer(basket)
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {
                            'quantity':
                                f'Максимальное количество товара '
                                f'{product.quantity}.'
                                f'В корзине {basket.quantity}.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except KeyError:
            return Response(
                {'product_id': 'Поле обязательно к заполнению'},
                status=status.HTTP_400_BAD_REQUEST
            )
