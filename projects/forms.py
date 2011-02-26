from django import forms

from translator.projects.models import Project

class ProjectForm(forms.ModelForm):
    #name = forms.CharField()
    #description = forms.CharField(widget=forms.Textarea)
    #url = forms.URLField()
    
    class Meta:
        model = Project
        fields = ('name', 'description', 'url', 'base_locale')

