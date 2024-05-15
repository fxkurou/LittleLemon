from rest_framework import serializers
from .models import (Category, MenuItem, Cart, Order, OrderItem)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'inventory': {'min_value': 0}
        }


class CartSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menu_item', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']


class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'user', 'order', 'menu_item', 'quantity', 'unit_price', 'price']
