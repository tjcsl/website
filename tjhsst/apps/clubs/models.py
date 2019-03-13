from django.db import models

# Create your models here.
class Clubs(models.Model);
    name = models.CharField(max_length=100, primary_key = True)
    image = models.ImageField(upload_to = "club_photos/")
    description = models.CharField(max_length=5000)
    link = models.CharField(max_length=200, blank = True, height_field = height, width_field = width)
    
    width = models.IntegerField()
    height = models.IntegerField()
    
