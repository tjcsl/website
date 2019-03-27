from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Club(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=100, unique = True)
    url = models.CharField(max_length=10, unique = True, validators=[RegexValidator(regex="^[a-zA-Z0-9_]+$", message="Only alphanumeric and underscores allowed")])
    height = models.IntegerField()
    width = models.IntegerField()
    image = models.ImageField(upload_to = "club_photos/", height_field = "height", width_field = "width")
    description = models.CharField(max_length=5000)
    link = models.CharField(max_length=200, blank = True)
    
    category = models.ForeignKey("Category", related_name="clubs", on_delete=models.SET_NULL, blank = True, null = True)
    keywords = models.ManyToManyField("Keyword", related_name="clubs")

    def __str__(self):
        return self.name

class Keyword(models.Model):
    name = models.CharField(max_length=20, primary_key = True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=20, primary_key = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
