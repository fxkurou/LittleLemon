from django.urls import path
from .views import secret, Home
from .views import (MenuItemsView, SingleMenuItemView, CategoriesView, CartView, OrderItemView, OrderView)

urlpatterns = [
    path('secret/', secret),
    path('home/', Home.as_view()),
    path('menu-items/', MenuItemsView.as_view()),
    path('category/', CategoriesView.as_view()),
    path('menu-items/<int:pk>/', SingleMenuItemView.as_view()),
    path('cart/menu-items/', CartView.as_view()),
    # path('cart/menu-items/', CartDetailView.as_view()),
    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>/', OrderItemView.as_view()),
]