from django import http
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import check_for_language

from translator.projects.models import Project
from translator.projects.forms import ProjectForm
from translator.strings.models import String, Translation
import reversion

def index(request):
    projects = Project.objects.all()

    return render_to_response('projects/index.html', {
        'projects': projects,
    }, context_instance=RequestContext(request))

def new(request):
    form = ProjectForm()
    return render_to_response('projects/new.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def create(request):
    assert request.method == 'POST'
    form = ProjectForm(request.POST)
    messages = []
    if form.is_valid():
        project = form.save()
        messages.append(_('Your new project has been created.'))
        return http.HttpResponseRedirect('/projects/')
    else:
        messages.append(_("There was a problem creating your project."))
    return render_to_response('projects/new.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def show(request, slug):
    project = get_object_or_404(Project, slug=slug)
    translated_strings = String.objects.filter(project=project.id, translated=True)
    untranslated_strings = String.objects.filter(project=project.id, translated=False)

    def assign_translations(strings):
        for string in strings:
            string.base_locale = string.translation_set.filter(locale=project.base_locale).latest('id').text
            string.target_locale = string.translation_set.filter(locale=request.session['target_locale']).latest('id').text

    assign_translations(translated_strings)
    assign_translations(untranslated_strings)

    context = {
        'project': project,
        'translated_strings': translated_strings,
        'untranslated_strings': untranslated_strings,
    }
    return render_to_response('projects/show.html', context,
                          context_instance=RequestContext(request))

#TODO: move to better location
def set_locale(request, locale):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = http.HttpResponseRedirect(next)
    if locale and check_for_language(locale):
        request.session['django_language'] = locale
    return response

def set_target_locale(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        request.session['target_locale'] = lang_code
    return response

