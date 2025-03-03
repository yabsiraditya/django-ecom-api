from django.contrib import admin
from api.models import Order, OrderItem, User, Product


class OrderItemInLine(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInLine
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Product)