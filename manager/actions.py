# -*- coding: utf-8 -*-

# from http://weitlandt.com/theme/2010/05/wir-djangonauten-csv-export-nach-excel-mit-umlauten/

import csv, codecs, time

#from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _

def get_csv_from_dict_list(field_list, data):
    csv_line = ";".join(['{{ row.%s|addslashes }}' % field for field in field_list])
    template = "{% for row in data %}" + csv_line + "\n{% endfor %}"
    return Template(template).render(Context({"data" : data}))

def export_csv(modeladmin, request, queryset):
    #if not request.user.is_staff:
    #    raise PermissionDenied

    replace_dc = { '\n' : '* ', '\r' : '', ';' : ',', '\"' : '|', '\'' : '|'}
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s_%s.csv' % (unicode(opts).replace('.', '_'), time.strftime('%Y%m%d-%H%M%S', time.localtime()))
    w = csv.writer(response, delimiter=';')
    field_names = [field.name for field in opts.fields]
    w.writerow(field_names)
    ax = []
    for obj in queryset:
        acc = {}
        for field in field_names:
            uf = unicode(getattr(obj, field))
            for i, j in replace_dc.iteritems():
                uf = uf.replace(i,j)
                acc[field] = uf
        ax.append(acc)
    response.write (get_csv_from_dict_list(field_names, ax))
    #response.write (get_csv_from_dict_list(field_names, ax).encode("iso-8859-15"))
    return response

export_csv.short_description = _(u"Export in CSV format")
