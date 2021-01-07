from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class loc(models.Model):
	bno = models.CharField(max_length = 200)
	street = models.CharField(max_length = 200)
	area = models.CharField(max_length = 200)
	state = models.CharField(max_length = 200)
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	
	def __str__(self):
		return self.area