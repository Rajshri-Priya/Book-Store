from django.db import models
from user_auth.models import CustomUser
from book.models import Book


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=7, default='active')

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # related_name='items'
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in {self.cart.user.username}'s Cart"


class Ordered(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Ordered"


class OrderedItem(models.Model):
    ORDERED = 'ordered'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (ORDERED, 'Ordered'),
        (CANCELLED, 'Cancelled'),
    ]
    ordered = models.ForeignKey(Ordered, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(choices=STATUS_CHOICES, default=ORDERED, max_length=10)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in {self.ordered.user.username}'s Order"


