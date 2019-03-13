from django.db import models

# Create your models here.
class Club(models.Model):
    name = models.Charfield(max_length=100, primary_key=True)
    description = models.Charfield(max_length=5000)
    link = models.Charfield(max_length=200, blank=True)
    image = models.ImageField(upload_to="club_photos/", height_field=height, width_field=width)
    width = models.IntegerField()
    height = models.IntegerField()