# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import *
from forms import *

class TopicAdmin(admin.ModelAdmin):
    form = TopicAdminForm
    list_display = ('label', 'email')
    search_fields = ('topiclabel__value', 'email')
admin.site.register(Topic, TopicAdmin)

class LanguageAdmin(admin.ModelAdmin):
    form = LanguageAdminForm
admin.site.register(Language, LanguageAdmin)

class CountryAdmin(admin.ModelAdmin):
    form = CountryAdminForm
    ordering = ('code',)
    search_fields = ('countrylabel__value', 'code',)
    list_display = ('label', 'code')
admin.site.register(Country, CountryAdmin)

class LicenseAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
admin.site.register(License, LicenseAdmin)

class TransportationAdmin(admin.ModelAdmin):
    form = TransportationAdminForm
admin.site.register(Transportation, TransportationAdmin)

class TalkAdmin(admin.ModelAdmin):
    form = TalkAdminForm
    list_filter = ('status', 'nature', 'language', 'charges', 'topic')
    search_fields = ('title', 'speakers', 'abstract', 'constraints', 'biography')
    list_display = ('title', 'date', 'language', 'speakers', 'capture', 'charges', 'city', 'country', 'cost')
admin.site.register(Talk, TalkAdmin)
