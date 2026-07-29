from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:product_id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:product_id>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:product_id>/', views.remove_item, name='remove_item'),
    path('clear/', views.clear_cart, name='clear_cart'),
]