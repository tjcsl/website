from django.contrib import admin
from .models import Lab, Prerequisite, Recommended
# Register your models here.
admin.site.register(Lab)
admin.site.register(Prerequisite)
admin.site.register(Recommended)