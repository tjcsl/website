from django import forms

from .models import Announcement, Category, Club, Keyword


class AnnouncementCreationForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "content", "club"]
        widgets = {
            "content": forms.Textarea(attrs={"cols": 40, "rows": 3}),
            "club": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["club"].label = ""


class ClubForm(forms.ModelForm):
    link = forms.URLField(required=False)
    category = forms.ModelChoiceField(Category.objects.all(), required=True, empty_label=None)
    keywords = forms.ModelMultipleChoiceField(Keyword.objects.all(), required=False)

    class Meta:
        model = Club
        fields = ["name", "image", "description", "link", "category", "keywords", "activity_id"]
        widgets = {"description": forms.Textarea(attrs={"cols": 40, "rows": 3})}


class ClubCreationForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "url", "admins"]
