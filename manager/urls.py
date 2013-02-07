# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to

from manager.views import new, end

urlpatterns = patterns ('',
    url(r'^new$', new, {'tmpl': 'manager/new.html'}),
    url(r'^end$', end, {'tmpl': 'manager/end.html'}),
    url(r'^closed$', end, {'tmpl': 'manager/closed.html'}),
)
