# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from cfp.manager.views import *

urlpatterns = patterns ('',
    url(r'^new$', new, {'tmpl': 'manager/new.html'}),
    url(r'^end$', end, {'tmpl': 'manager/end.html'}),
    url(r'^closed$', end, {'tmpl': 'manager/closed.html'}),
)
