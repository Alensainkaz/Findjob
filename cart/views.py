from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from resume.models import Resume
from .models import Cart, CartItem


def ensure_cart(user):
    # get_or_create retries the lookup on IntegrityError, so concurrent requests share one cart
    cart, _created = Cart.objects.get_or_create(user=user)
    return cart


def _wants_json(request):
    return 'application/json' in request.headers.get('Accept', '')


@login_required
def cart_detail(request):
    cart = ensure_cart(request.user)
    items = cart.items.select_related('resume').order_by('-id')
    payload = [{
        'id': item.pk,
        'resumeId': item.resume_id,
        'name': item.resume.name,
        'surname': item.resume.surname,
        'speciality': item.resume.get_speciality_display(),
        'email': item.resume.email,
        'image': item.resume.image.url if item.resume.image else '',
        'url': reverse('resume_detail', args=[item.resume_id]),
        'removeUrl': reverse('cart_remove', args=[item.pk]),
    } for item in items]
    return render(request, 'cart_detail.html', {
        'items': items,
        'props': {'items': payload, 'browseUrl': reverse('index')},
    })


@login_required
@require_POST
def cart_add(request, item_id):
    cart = ensure_cart(request.user)
    resume = get_object_or_404(Resume, id=item_id)
    CartItem.objects.get_or_create(cart=cart, resume=resume)
    if _wants_json(request):
        return JsonResponse({'saved': True})
    next_url = request.POST.get('next', '')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = 'cart_detail'
    return redirect(next_url)


@login_required
@require_POST
def cart_toggle(request, resume_id):
    """Save or unsave a resume; used by the resume board."""
    resume = get_object_or_404(Resume, id=resume_id)
    cart = ensure_cart(request.user)
    deleted, _ = CartItem.objects.filter(cart=cart, resume=resume).delete()
    if not deleted:
        CartItem.objects.get_or_create(cart=cart, resume=resume)
    return JsonResponse({'saved': not deleted})


@login_required
@require_POST
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    if _wants_json(request):
        return JsonResponse({'removed': True})
    return redirect('cart_detail')
