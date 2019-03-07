from django.db import models

# Create your models here.

class TagCategory(models.Model):
    name = models.CharField(max_length = 30)

class Tag(models.Model):
    name = models.CharField(max_length = 30)

    category = models.ForeignKey(TagCategory, related_name = "tags", on_delete = models.CASCADE)

