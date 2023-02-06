from rest_framework import serializers, fields

from products.models import Product, Image, Basket


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Image
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        depth = 1
        fields = (
            'id',
            'name',
            'description',
            'price',
            'quantity',
            'images',
            'category'
        )


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = (
            'id', 'product', 'quantity', 'sum', 'total_sum',
            'total_quantity', 'created_timestamp'
        )
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()

    def validate(self, data):
        if self.partial:
            product = Product.objects.filter(id=self.instance.product_id).first()
            if data['quantity'] > product.quantity:
                raise serializers.ValidationError(
                    f'Количество товара на складе {product.quantity}'
                )
            return data












    



