from django.conf import settings

def django_conf(request):
    if not 'django_language' in request.session:
        request.session['django_language'] = settings.LANGUAGE_CODE
    if not 'target_locale' in request.session:
        request.session['target_locale'] = 'fr-fr'
    return {
        'settings': settings,
        'BASE_LOCALE_NAME': 'English',
        'LOCALE': request.session['django_language'],
        'TARGET_LOCALE': request.session['target_locale'],
        'TARGET_LOCALE_NAME': settings.LANGUAGE_NAMES[request.session['target_locale']],
        'CURRENT_URL': request.path,
    }
