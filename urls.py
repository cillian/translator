from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^translator/', include('translator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^projects/', include('projects.urls')),
    (r'^strings/', include('strings.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^accounts/', include('registration.urls')),
    url(r'^$',    'projects.views.index', name='projects_index'),
)

#if settings.DEBUG:
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
urlpatterns += patterns('',
    (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
     { 'document_root': settings.MEDIA_ROOT }
    ),
)
