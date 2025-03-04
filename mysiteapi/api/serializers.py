from django.db import transaction
from rest_framework import serializers
from .models import Product, Order, OrderItem, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'user_permissions', 'is_authenticated', 'get_full_name', 'orders')
        # fields = (
        #     'username',
        #     'email',
        #     'is_staff',
        #     'is_superuser'
        # )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'description',
            'name', 
            'price', 
            'stock', 
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater thn 0"
            )
        return value
    

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        source='product.price', 
        max_digits=13, 
        decimal_places=2,
    )

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem   
            fields = (
                'product',
                'quantity',
            )

    order_id = serializers.UUIDField(read_only=True,)
    items = OrderItemCreateSerializer(many=True, required=False)
    
    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if orderitem_data is not None:
                instance.items.all().delete()
                for item  in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)
        return instance


    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)
        return order

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items',
        )
        extra_kwargs = {
            'user':{'read_only':True}
        }


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True,)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price',
        )

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()