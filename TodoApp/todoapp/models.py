from django.db import models

# Create your models here.
class Todo(models.Model):
  add_date = models.DateTimeField()
  content = models.CharField(max_length=200)