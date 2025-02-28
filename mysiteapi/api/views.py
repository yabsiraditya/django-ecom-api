from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerialize, OrderItemSerialize, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.exclude(stock__gt=0)
    serializer_class = ProductSerializer


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


class OrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerialize
    

class UserOrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerialize
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price'],
    })
    return Response(serializer.data)