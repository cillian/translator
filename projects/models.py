from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField()
    slug = models.SlugField(unique=True)
    base_locale = models.CharField(max_length=8, choices=settings.LANGUAGES)

    def save(self):
        self.slug = slugify( self.name )
        super( Project, self ).save()

