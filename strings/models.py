from django.db import models
import reversion

class String(models.Model):
    group = models.CharField(max_length=50)
    project = models.ForeignKey('projects.Project')
    translated = models.BooleanField()

class Translation(models.Model):
    string = models.ForeignKey('String')
    locale = models.CharField(max_length=8)
    text = models.TextField()

#if not reversion.is_registered(Translation):
#    reversion.register(Translation)

from django.contrib import admin

from reversion.admin import VersionAdmin
#from yoursite.models import YourModel

class TranslationAdmin(VersionAdmin):
    """Admin settings go here."""

if not reversion.is_registered(Translation):
    admin.site.register(Translation, TranslationAdmin)
