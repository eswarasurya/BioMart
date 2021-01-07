from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Product(models.Model):
    productid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=100)
    mrp = models.FloatField()
    discount = models.FloatField()
    price = models.FloatField()
    quantity = models.FloatField(blank=True)
    origin = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product_name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    stars = models.FloatField()
    reviewby = models.ForeignKey(User, on_delete=models.CASCADE)

