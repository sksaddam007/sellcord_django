# disputes/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Seller, Item, Order, Return, Dispute


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'seller')
    search_fields = ('name', 'description', 'seller__name')
    list_filter = ('seller',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'date_ordered')
    search_fields = ('customer', 'item__name')
    list_filter = ('item',)


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('order', 'return_reason', 'return_tracking', 'date_returned')
    search_fields = ('order__customer_name', 'return_reason', 'return_tracking')
    list_filter = ('order',)


@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('return_order', 'dispute_reason', 'status', 'date_created', 'date_updated')
    search_fields = ('return_order__order__customer_name', 'dispute_reason', 'status')
    list_filter = ('status', 'return_order')
