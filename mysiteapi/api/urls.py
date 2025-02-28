from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListApiView.as_view()),
    path('products/info/', views.product_info),
    path('products/<int:product_id>/', views.ProductDetailApiView.as_view()),
    path('orders/', views.OrderListApiView.as_view()),
]