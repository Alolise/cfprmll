# -*- coding: utf-8 -*-

import os
import sys

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.management.base import BaseCommand

from manager.models import Country


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        countries_data_file = os.path.join(settings.PROJECT_DIR, "datas", "countries.csv")
        if not os.path.exists(countries_data_file):
            print "Error: '%s' does not exist" % countries_data_file
            return

        data = open(countries_data_file, "r").readlines()
        a = 0
        total = len(data)
        for i in data:
            a += 1
            sys.stdout.write("%s/%s\r" % (a, total))
            sys.stdout.flush()
            lbls = {}
            code, lbls['en'], lbls['fr'], lbls['sp'] = i.split(';')
            try:
                country = Country.objects.get(code=code)
            except ObjectDoesNotExist:
                country = Country.objects.create(code=code)
            for lang in lbls:
                country.set_label(value=lbls[lang], lang=lang)

        sys.stdout.write("\n")
