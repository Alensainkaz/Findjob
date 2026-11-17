from django.db import migrations, models


def dedupe(apps, schema_editor):
    """Merge duplicate carts per user and drop duplicate saved resumes before adding the constraints."""
    Cart = apps.get_model('cart', 'Cart')
    CartItem = apps.get_model('cart', 'CartItem')

    user_ids = Cart.objects.exclude(user=None).values_list('user_id', flat=True).distinct()
    for user_id in user_ids:
        carts = list(Cart.objects.filter(user_id=user_id).order_by('id'))
        keep, extras = carts[0], carts[1:]
        if extras:
            CartItem.objects.filter(cart__in=extras).update(cart=keep)
            Cart.objects.filter(id__in=[c.id for c in extras]).delete()

    seen = set()
    for item in CartItem.objects.order_by('id').only('id', 'cart_id', 'resume_id'):
        key = (item.cart_id, item.resume_id)
        if key in seen:
            item.delete()
        else:
            seen.add(key)


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_cartitem_item_cartitem_resume_and_more'),
    ]

    operations = [
        migrations.RunPython(dedupe, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(condition=models.Q(user__isnull=False), fields=('user',), name='cart_one_per_user'),
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(fields=('cart', 'resume'), name='cartitem_unique_resume'),
        ),
    ]
