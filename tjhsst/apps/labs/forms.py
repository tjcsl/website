from django import forms

from .models import Course, Lab, Project, Testimonial


class LabForm(forms.ModelForm):
    link = forms.URLField(required=False)
    prerequisites = forms.ModelMultipleChoiceField(Course.objects.all(), required=False)
    recommended = forms.ModelMultipleChoiceField(Course.objects.all(), required=False)

    class Meta:
        model = Lab
        fields = ["name", "image", "description", "link", "prerequisites", "recommended"]
        widgets = {"description": forms.Textarea(attrs={"cols": 40, "rows": 3})}


class LabCreationForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ["name", "url", "admins"]


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "labs", "authors", "image", "description"]
        widgets = {"description": forms.Textarea(attrs={"cols": 40, "rows": 3})}


class TestimonialCreationForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["lab", "content"]
        widgets = {"description": forms.Textarea(attrs={"cols": 40, "rows": 3})}
