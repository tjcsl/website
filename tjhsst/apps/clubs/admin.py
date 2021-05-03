from django.contrib import admin

from .models import Announcement, Category, Club, Keyword

# Register your models here.
admin.site.register(Announcement)
admin.site.register(Club)
admin.site.register(Keyword)
admin.site.register(Category)
