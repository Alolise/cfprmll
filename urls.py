# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    # admin interface
    (r'^admin/(.*)', admin.site.root),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^$', redirect_to, {'url': 'talk/new'}),
    (r'^talk/', include('cfp.manager.urls')),
)

if settings.DEBUG:
    import os.path
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DOCUMENT_ROOT}),
    )
