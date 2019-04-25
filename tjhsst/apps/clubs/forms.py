from django import forms

from .models import Club, Keyword, Category

class ClubForm(forms.ModelForm):
    link = forms.URLField()
    category = forms.ModelChoiceField(Category.objects.all(), required = True, empty_label = None)
    keywords = forms.ModelMultipleChoiceField(Keyword.objects.all(), required = True)

    class Meta:
        model = Club
        fields = ["name", "url", "image", "description", "link", "category", "keywords"]
        widgets = {
            "description": forms.Textarea(attrs = {"cols": 40, "rows": 3}),
        }

