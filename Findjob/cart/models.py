from django.db import models
from resume.models import Resume

class Cart(models.Model):
    user = models.ForeignKey('users.User', null=True, related_name='carts', on_delete=models.CASCADE)

    def __str__(self):
        return f'Cart of {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cart.user.username} - {self.resume}'