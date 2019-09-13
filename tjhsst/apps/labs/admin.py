from django.contrib import admin

from .models import Course, Lab

# Register your models here.
admin.site.register(Lab)
admin.site.register(Course)
