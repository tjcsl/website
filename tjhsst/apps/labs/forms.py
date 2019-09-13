from django import forms

from .models import Course, Lab


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
