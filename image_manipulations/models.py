from django.db import models

# Create your models here.

class Tags(models.Model):
    name = models.CharField(max_length=100)

class Image_gallery(models.Model):
    image = models.ImageField(upload_to="image")
    tags = models.ManyToManyField(Tags)
    