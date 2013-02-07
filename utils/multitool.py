# -*- coding: utf-8 -*-

import sys, os.path

######################
sys.path.append(os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../../'))
os.environ['DJANGO_SETTINGS_MODULE'] ='cfp.settings'

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import setup_environ
from django.conf import settings
######################

from manager.models import Country

#####################
setup_environ(settings)
#####################

class CountryImport:
    @staticmethod
    def from_csv(fcsv):
        if os.path.exists(fcsv):
            handle = file(fcsv)
            for i in handle.readlines():
                lbls = {}
                code, lbls['en'], lbls['fr'], lbls['sp'] = i.split(';')
                try:
                    country = Country.objects.get(code=code)
                except ObjectDoesNotExist:
                    country = Country.objects.create(code=code)
                for lang in lbls:
                    country.set_label(value=lbls[lang], lang=lang)
        else:
            print "Err: unable to find file '%s'" % fcsv

if __name__ == "__main__":
    ok = False
    args = ['importcountries']
    if len(sys.argv) > 1 and sys.argv[1] in args:
        ok = True
        if sys.argv[1] == 'importcountries' and len(sys.argv) > 2:
            CountryImport.from_csv(sys.argv[2])
        else:
            ok = False

    if not ok:
        print 'Usage: %s %s' % (sys.argv[0], "|".join(args))
