from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    para = models.CharField(max_length=20000000)
    created = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.title