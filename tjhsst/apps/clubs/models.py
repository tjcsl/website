from django.db import models

# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=100, primary_key = True)
    height = models.IntegerField()
    width = models.IntegerField()
    image = models.ImageField(upload_to = "club_photos/", height_field = height, width_field = width)
    description = models.CharField(max_length=5000)
    link = models.CharField(max_length=200, blank = True)    
