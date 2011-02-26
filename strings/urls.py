from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
  url(r'^new/project/(?P<project_slug>[\w-]+)/$',
      'strings.views.new',
      name='strings_new'),
  url(r'^create/project/(?P<project_slug>[\w-]+)/$',
      'strings.views.create',
      name='strings_create'),
)
