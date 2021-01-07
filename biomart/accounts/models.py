from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=True)
    cart_items = ArrayField(models.CharField(max_length=100), blank=True)
    brought_items = ArrayField(models.CharField(max_length=100), blank=True)


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=True)
    cart_items = ArrayField(models.CharField(max_length=100), blank=True)
    sell_items = ArrayField(models.CharField(max_length=100), blank=True)
    sold_items = ArrayField(models.CharField(max_length=100), blank=True)
    brought_items = ArrayField(models.CharField(max_length=100), blank=True)
    