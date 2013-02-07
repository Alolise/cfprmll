# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect

from django.conf import settings
from utils.decorators import auto_render

from forms import TalkForm

from datetime import datetime

@auto_render
def new(request, tmpl):
    syserr = None

    limit = datetime.strptime(settings.CFP_LIMIT_DATE, '%Y-%m-%d %H:%M:%S')
    if datetime.utcnow() > limit:
        return HttpResponseRedirect('/talk/closed')

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
