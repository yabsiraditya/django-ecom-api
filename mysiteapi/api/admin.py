from django.contrib import admin
from api.models import Order, OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInLine
    ]

admin.site.register(Order, OrderAdmin)