# -*- coding: utf-8 -*-

# from http://weitlandt.com/theme/2010/05/wir-djangonauten-csv-export-nach-excel-mit-umlauten/

import csv, codecs, time

from django.http import HttpResponse
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _

def export_csv(modeladmin, request, queryset):
    replace_dc = { '\n' : u'¬', '\r' : ''}
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s_%s.csv' % (unicode(opts).replace('.', '_'), time.strftime('%Y%m%d-%H%M%S', time.localtime()))
    w = csv.writer(response, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    field_names = [field.name for field in opts.fields]
    w.writerow(field_names)
    for obj in queryset:
        fields = []
        for field in field_names:
            value = unicode(getattr(obj, field))
            for i, j in replace_dc.iteritems():
                value = value.replace(i, j)
            fields.append(value.encode('utf-8'))
        w.writerow(fields)
    return response

export_csv.short_description = _(u"Export in CSV format")
