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
    path('edit_dispute/<int:dispute_id>/', views.edit_dispute, name='edit_dispute'),
    path('delete_dispute/<int:dispute_id>/', views.delete_dispute, name='delete_dispute'),
    path('create_item/', views.create_item, name='create_item'),
    path('edit_item/<int:item_id>', views.edit_item, name='edit_item'),
    path('order/create/<int:item_id>/', views.create_order, name='create_order'),
    path('orders/edit/<int:order_id>/', views.edit_order, name='edit_order'),

]
