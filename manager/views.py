# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect

from cfp import settings
from cfp.utils.decorators import auto_render

from forms import TalkForm

@auto_render
def new(request, tmpl):
    syserr = None
    if request.method == 'POST':
        form = TalkForm(request.POST)
        if form.is_valid():
            if form.save():
                return HttpResponseRedirect('/talk/end')
            else:
                syserr = True
    else:
        form = TalkForm()
    return tmpl, locals()

@auto_render
def end(request, tmpl):
    return tmpl, locals()