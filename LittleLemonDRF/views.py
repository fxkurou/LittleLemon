from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import (Category, MenuItem, Cart, Order, OrderItem)
from .serializers import (MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer)


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'title']
    filterset_fields = ['title', 'price', 'featured']
    search_fields = ['title', 'category']

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'title']
    filterset_fields = ['title', 'price', 'featured']
    search_fields = ['title', 'category']


class CartView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        menu_item = serializer.validated_data['menu_item']
        quantity = serializer.validated_data['quantity']
        serializer.save(user=self.request.user, price=menu_item.price*quantity, unit_price=menu_item.price)


# class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = 0
        for cart_item in cart_items:
            total += cart_item.price
        serializer.save(user=self.request.user, total=total)


class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = Order.objects.get(id=self.request.data['order'])
        menu_item = serializer.validated_data['menu_item']
        quantity = serializer.validated_data['quantity']
        serializer.save(order=order, price=menu_item.price*quantity, unit_price=menu_item.price)


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


@api_view()
def secret(request):
    return Response({'message':'You have accessed the secret view'})