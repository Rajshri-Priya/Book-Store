from django.db import models
from user_auth.models import CustomUser


# Create your models here.
class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
