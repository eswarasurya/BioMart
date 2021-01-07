from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class blog(models.Model):
	title = models.CharField(max_length = 200)
	body = models.TextField()
	writer = models.ForeignKey(User, on_delete = models.CASCADE)
	pub_date = models.DateTimeField(default=datetime.now(), blank=True)
	
	def pub_date_pretty(self):
		return self.pub_date.strftime('%b %e %Y')
