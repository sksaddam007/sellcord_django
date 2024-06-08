# disputes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('items/', views.item_list, name='item_list'),
    path('orders/', views.order_list, name='order_list'),
    path('returns/', views.return_list, name='return_list'),
    path('disputes/', views.dispute_list, name='dispute_list'),
    path('create_dispute/<int:return_id>/', views.create_dispute, name='create_dispute'),
    path('create_item/', views.create_item, name='create_item'),
    path('create_order/', views.create_order, name='create_order'),

]
