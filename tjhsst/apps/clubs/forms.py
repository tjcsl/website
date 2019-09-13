from django import forms

from .models import Category, Club, Keyword


class ClubForm(forms.ModelForm):
    link = forms.URLField(required = False)
    category = forms.ModelChoiceField(Category.objects.all(), required = True, empty_label = None)
    keywords = forms.ModelMultipleChoiceField(Keyword.objects.all(), required = False)

    class Meta:
        model = Club
        fields = ["name", "image", "description", "link", "category", "keywords"]
        widgets = {
            "description": forms.Textarea(attrs = {"cols": 40, "rows": 3}),
        }

class ClubCreationForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "url", "admins"]
