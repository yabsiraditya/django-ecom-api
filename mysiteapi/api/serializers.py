from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name', 
            'description', 
            'price', 
            'stock', 
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater thn 0"
            )
        return value
    

class OrderItemSerialize(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
        )


class OrderSerialize(serializers.ModelSerializer):
    items = OrderItemSerialize(many=True, read_only=True)
    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
        )
    
    def validate_(self, value):
        pass