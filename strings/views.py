from django import http
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

import reversion
from reversion.models import Version, Revision

from translator.projects.models import Project
from translator.strings.models import String, Translation
from translator.strings.forms import StringForm, TranslationForm

def new(request, project_slug):
  string_form = StringForm()
  project = get_object_or_404(Project, slug=project_slug)
  base_locale_translation_form = TranslationForm(prefix='base-locale', initial={
      'locale': project.base_locale,
  })
  target_locale_translation_form = TranslationForm(prefix='target-locale', initial={
      'locale': request.session['target_locale'],
  })
  
  return render_to_response('strings/new.html', {
      'string_form': string_form,
      'base_locale_translation_form': base_locale_translation_form,
      'target_locale_translation_form': target_locale_translation_form,
      'project': project, 
  }, context_instance=RequestContext(request))

def create(request, project_slug):
    assert request.method == 'POST'
    project = get_object_or_404(Project, slug=project_slug)

    string_form = StringForm(request.POST)
    base_locale_translation_form = TranslationForm(request.POST, prefix='base-locale')
    target_locale_translation_form = TranslationForm(request.POST, prefix='target-locale')
    messages = []
    if string_form.is_valid() and base_locale_translation_form.is_valid() and target_locale_translation_form.is_valid():
        string = string_form.save(commit=False)
        string.project = project
        string.save()

        base_locale_translation = base_locale_translation_form.save(commit=False)
        base_locale_translation.string = string
        base_locale_translation.save()

      # TODO: target should be optional when creating a new string.
        target_locale_translation = target_locale_translation_form.save(commit=False)
        target_locale_translation.string = string
        target_locale_translation.save()

        # Create translation for all other languages.
        for lang in settings.LANGUAGES:
            if lang[0] != project.base_locale and (lang[0] != request.session['target_locale']):
                translation = Translation(text='', locale=lang[0])
                translation.string = string
                translation.save()

        messages.append(_('Your new string has been created.'))
        return http.HttpResponseRedirect(
            reverse('projects_show', kwargs=dict(slug=project.slug)))
    else:
        messages.append(_("There was a problem creating your string."))
    return render_to_response('strings/new.html', {
        'string_form': string_form,
        'base_locale_translation_form': base_locale_translation_form,
        'target_locale_translation_form': target_locale_translation_form,
        'project': project,
    }, context_instance=RequestContext(request))

def edit(request, project_slug, string_id):
    string = get_object_or_404(String, id=string_id)
    project = get_object_or_404(Project, slug=project_slug)
    base_locale_translation = Translation.objects.order_by('-date_created').get(string=string, locale=project.base_locale)        
    target_locale_translation = Translation.objects.order_by('-date_created').get(string=string, locale=request.session['target_locale'])
    versions = Version.objects.get_for_object(target_locale_translation).order_by('-id')

    if request.method == 'POST':
        string_form = StringForm(request.POST, instance=string)
        base_locale_translation_form = TranslationForm(request.POST, instance=base_locale_translation, prefix="base-locale")
        target_locale_translation_form = TranslationForm(request.POST, instance=target_locale_translation, prefix="target-locale")
        messages = []

        if string_form.is_valid() and base_locale_translation_form.is_valid() and target_locale_translation_form.is_valid():
            string = string_form.save(commit=False)
            string.project = project
            string.save()

            base_locale_translation = base_locale_translation_form.save(commit=False)
            base_locale_translation.string = string
            with reversion.revision:
                base_locale_translation.save()

            target_locale_translation = target_locale_translation_form.save(commit=False)
            target_locale_translation.string = string
            with reversion.revision:
                target_locale_translation.save()

        return http.HttpResponseRedirect(
            reverse('projects_show', kwargs=dict(slug=project.slug)))
    else:
        string_form = StringForm(instance=string)
        base_locale_translation_form = TranslationForm(instance=base_locale_translation, prefix="base-locale")
        target_locale_translation_form = TranslationForm(instance=target_locale_translation, prefix="target-locale")
        return render_to_response('strings/edit.html', {
            'string': string,
            'project': project,
            'string_form': string_form,
            'base_locale_translation_form': base_locale_translation_form,
            'target_locale_translation_form': target_locale_translation_form,
            'versions': versions,
        }, context_instance=RequestContext(request))

def show_version(request, project_slug, string_id, version_id):
    string = get_object_or_404(String, id=string_id)
    project = get_object_or_404(Project, slug=project_slug)
    version = get_object_or_404(Version, id=version_id)
    base_locale_translation = Translation.objects.order_by('-date_created').get(string=string, locale=project.base_locale)        
    versions = Version.objects.get_for_object_reference(Translation, version.object_id).order_by('-id')

    string_form = StringForm(instance=string)
    string_form.fields['group'].widget.attrs['disabled'] = True
    string_form.fields['translated'].widget.attrs['disabled'] = True
    base_locale_translation_form = TranslationForm(instance=base_locale_translation, prefix="base-locale")
    base_locale_translation_form.fields['text'].widget.attrs['disabled'] = True
    target_locale_translation_form = TranslationForm(initial={
        'text': version.field_dict['text']
    })
    target_locale_translation_form.fields['text'].widget.attrs['disabled'] = True
    
    return render_to_response('strings/show_revision.html', {
        'string': string,
        'project': project,
        'version': version,
        'string_form': string_form,
        'base_locale_translation_form': base_locale_translation_form,
        'target_locale_translation_form': target_locale_translation_form,
        'versions': versions,
    }, context_instance=RequestContext(request))


def revert(request, project_slug, string_id, version_id):
    string = get_object_or_404(String, id=string_id)
    project = get_object_or_404(Project, slug=project_slug)
    version = get_object_or_404(Version, id=version_id)
    version.revert()
    return http.HttpResponseRedirect(reverse('projects_show', kwargs=dict(slug=project.slug)))
