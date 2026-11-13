from django.contrib import admin
from django.db.models import Count
from unfold.admin import ModelAdmin, TabularInline

from .models import Cart, CartItem


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ('resume',)


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user', 'items_count')
    search_fields = ('user__username', 'user__email')
    autocomplete_fields = ('user',)
    inlines = (CartItemInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(_items=Count('items'))

    @admin.display(description='Saved resumes', ordering='_items')
    def items_count(self, obj):
        return obj._items


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ('resume', 'cart')
    search_fields = ('resume__name', 'resume__surname', 'cart__user__username')
    autocomplete_fields = ('resume', 'cart')
