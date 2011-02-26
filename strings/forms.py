from django import forms

from strings.models import String, Translation

class StringForm(forms.ModelForm):
    class Meta:
        model = String
        fields = ["group", "translated"]

class TranslationForm(forms.ModelForm):
    locale = forms.Field(widget=forms.HiddenInput())
    
    class Meta:
        model = Translation
        fields = ["locale", "text"]
