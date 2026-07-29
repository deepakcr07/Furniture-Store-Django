from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_view, name='account'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('address/add/', views.add_address_view, name='add_address'),
    path('address/delete/<int:pk>/', views.delete_address_view, name='delete_address'),
    path('address/default/<int:pk>/', views.set_default_address_view, name='set_default_address'),
]