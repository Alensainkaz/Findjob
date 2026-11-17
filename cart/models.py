from django.db import models
from resume.models import Resume

class Cart(models.Model):
    user = models.ForeignKey('users.User', null=True, related_name='carts', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], condition=models.Q(user__isnull=False), name='cart_one_per_user'),
        ]

    def __str__(self):
        return f'Savings of {self.user.username if self.user else "(no user)"}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'resume'], name='cartitem_unique_resume'),
        ]

    def __str__(self):
        return f'{self.cart} - {self.resume}'