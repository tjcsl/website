from django.db import models

# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=100, primary_key = True)
    height = models.IntegerField()
    width = models.IntegerField()
    image = models.ImageField(upload_to = "club_photos/", height_field = height, width_field = width)
    description = models.CharField(max_length=5000)
    link = models.CharField(max_length=200, blank = True)    
    
    category = models.ForeignKey("Category", related_name="clubs", on_delete=models.SET_NULL, null = True)
    keywords = models.ManyToManyField("Keyword", related_name="clubs")

class Keyword(models.Model):
    name = models.CharField(max_length=20, primary_key = True)
    
class Category(models.Model):
    name = models.CharField(max_length=20, primary_key = True)
