from django.contrib import admin

from .models import Course, Lab, Project, Testimonial

# Register your models here.
admin.site.register(Lab)
admin.site.register(Course)
admin.site.register(Project)
admin.site.register(Testimonial)
