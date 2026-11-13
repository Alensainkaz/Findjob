from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from resume.models import Resume
from .models import Cart, CartItem


def ensure_cart(user):
    cart = Cart.objects.filter(user=user).first()
    if cart is None:
        cart = Cart.objects.create(user=user)
    return cart


@login_required
def cart_detail(request):
    cart = ensure_cart(request.user)
    items = cart.items.select_related('resume')
    context = {'items': items, 'cart': cart}
    return render(request, 'cart_detail.html', context)


@login_required
def cart_add(request, item_id):
    cart = ensure_cart(request.user)
    resume = get_object_or_404(Resume, id=item_id)
    CartItem.objects.get_or_create(cart=cart, resume=resume)
    return redirect('cart_detail')


@login_required
@require_POST
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')


@login_required
def cart_update(request, item_id):
    get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    return redirect('cart_detail')
