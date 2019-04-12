from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Lab(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=100, unique = True)
    url = models.CharField(max_length=20, unique = True, validators=[RegexValidator(regex="^[a-zA-Z0-9_\-]+$", message="Only alphanumeric, dashes, and underscores allowed")])

    height = models.IntegerField()
    width = models.IntegerField()
    image = models.ImageField(upload_to = "lab_photos/", height_field = "height", width_field = "width")

    description = models.CharField(max_length=5000)
    link = models.CharField(max_length=200, blank = True)
    
    prerequisites = models.ManyToManyField("Prerequisite", related_name="labs")
    recommended = models.ManyToManyField("Recommended", related_name="labs")
    app_label = "labs"
    
    def __str__(self):
        return self.name


class Recommended(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=20, unique = True)
    url = models.CharField(max_length=20, unique = True, validators=[RegexValidator(regex="^[a-zA-Z0-9_\-]+$", message="Only alphanumeric, dashes, and underscores allowed")])

    def __str__(self):
        return self.name
    

class Prerequisite(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=20, unique = True)
    url = models.CharField(max_length=20, unique = True, validators=[RegexValidator(regex="^[a-zA-Z0-9_\-]+$", message="Only alphanumeric, dashes, and underscores allowed")])

    def __str__(self):
        return self.name


