

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import MessageForm
from .models import Cart, CartItem
from resume.models import Resume

@login_required
def ensure_cart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    return cart
@login_required
def cart_detail(request):
    cart = ensure_cart(request)
    items=cart.items.all()
    context = {'items':items,'cart':cart}
    return render(request,'cart_detail.html',context)
@login_required
def cart_add(request,item_id):
    cart=ensure_cart(request)
    resume=get_object_or_404(Resume,id=item_id)
    item,created = CartItem.objects.get_or_create(cart=cart,resume=resume)
    item.save()
    return redirect('cart_detail')
@login_required
def cart_remove(request,item_id):
    item=get_object_or_404(CartItem,id=item_id,cart__user=request.user)
    item.delete()
    return redirect('cart_detail')
@login_required
def cart_update(request,item_id):
    item=get_object_or_404(CartItem,id=item_id,cart__user=request.user)
    return redirect('cart_detail')
@login_required
def message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.from_user = request.user
            message.save()
            return redirect('index')
    else:
        form=MessageForm()
    context = {'form':form}
    return render(request,'cart_message.html',context)

