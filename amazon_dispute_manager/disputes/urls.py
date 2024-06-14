# disputes/urls.py
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', login_required(lambda request: views.custom_login(request)), name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('items/', views.item_list, name='item_list'),
    path('orders/', views.order_list, name='order_list'),
    path('returns/', views.return_list, name='return_list'),
    path('create_return/<int:order_id>', views.create_return, name='create_return'),
    path('disputes/', views.dispute_list, name='dispute_list'),
    path('disputes/<int:dispute_id>', views.dispute_view, name='view_dispute'),
    path('create_dispute/<int:return_id>/', views.create_dispute, name='create_dispute'),
    path('edit_dispute/<int:dispute_id>/', views.edit_dispute, name='edit_dispute'),
    path('create_item/', views.create_item, name='create_item'),
    path('edit_item/<int:item_id>', views.edit_item, name='edit_item'),
    path('order/create/<int:item_id>/', views.create_order, name='create_order'),
    path('orders/edit/<int:order_id>/', views.edit_order, name='edit_order'),
    path('profile/', views.profile_view, name="profile"),
    path('<username>/', views.profile_view, name="userprofile"),
    path('profile/edit/', views.profile_edit_view, name="profile-edit"),
    path('profile/delete/', views.profile_delete_view, name="profile-delete"),
    path('profile/onboarding/', views.profile_edit_view, name="profile-onboarding"),

]
