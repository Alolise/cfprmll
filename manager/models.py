# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import get_language

from django.core.mail import send_mail, mail_admins
from django.template import Context, loader

from cfp import settings

class LabelClass:
    """
    Base class for a model which has a localized label
    """
    label_class = None
    labels = []

    def get_label_number(self, name):
        if not name:
            return 0
        labels = self.labels
        idx = 0
        for label_name, lbl in labels:
            if label_name == name:
                label_number = idx
            idx += 1
        return idx

    def label(self, name=None, lang=None):
        """
        Display the base accordingly to the language
        """
        label_class, labels = self.label_class, self.labels
        if not label_class:
            return u""
        label_number = self.get_label_number(name)
        if not lang or len(lang) < 2:
            lang = settings.LANGUAGES[0][0]
        default = u""
        try:
            lbl = label_class.objects.get(language=lang[:2],
                                  label_number=label_number, parent__id=self.id)
            if lbl and lbl.value:
                return lbl.value
            # langue par défaut si la langue n'est pas disponible
            lbl = label_class.objects.get(language=settings.LANGUAGES[0][0],
                                  label_number=label_number, parent__id=self.id)
            if lbl and lbl.value:
                return lbl.value
            return default
        except:
            return default

    def set_label(self, value, name=None, lang=None):
        """
        Update or create the label
        """
        label_class, labels = self.label_class, self.labels
        label_number = self.get_label_number(name)
        if not lang or len(lang) < 2:
            lang = settings.LANGUAGES[0][0]
        # try update
        try:
            lbl = label_class.objects.get(language=lang[:2],
                                  label_number=label_number, parent__id=self.id)
            lbl.value = value
            lbl.save()
        except ObjectDoesNotExist:
            label_class.objects.create(language=lang[:2], value=value,
                                         label_number=label_number, parent=self)

class BaseLabel(models.Model):
    """
    Abstract class for labels
    """
    language = models.CharField(_(u"Language"), max_length=2,
                                                    choices=settings.LANGUAGES)
    label_number = models.IntegerField()
    value = models.CharField(_(u"Value"), max_length=128)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.value


class TopicLabel(BaseLabel):
    parent = models.ForeignKey('Topic')

class Topic(models.Model, LabelClass):
    label_class = TopicLabel
    labels = (('lbl_name', _(u"Name")),)
    email = models.EmailField(_(u"Notice email"))
    def __unicode__(self):
        return self.label(lang=get_language())

class LanguageLabel(BaseLabel):
    parent = models.ForeignKey('Language')

class Language(models.Model, LabelClass):
    label_class = LanguageLabel
    labels = (('lbl_name', _(u"Name")),)
    def __unicode__(self):
        return self.label(lang=get_language())

class CountryLabel(BaseLabel):
    parent = models.ForeignKey('Country')

class Country(models.Model, LabelClass):
    label_class = CountryLabel
    labels = (('lbl_name', _(u"Name")),)
    code = models.CharField(_(u"Code"), max_length=2)
    def __unicode__(self):
        return self.label(lang=get_language())
    class Meta:
        verbose_name = _(u"Country")
        verbose_name_plural = _(u"Countries")

class License(models.Model):
    name = models.CharField(_(u"Name"), max_length=128)
    def __unicode__(self):
        return self.name

class TransportationLabel(BaseLabel):
    parent = models.ForeignKey('Transportation')

class Transportation(models.Model, LabelClass):
    label_class = TransportationLabel
    labels = (('lbl_name', _(u"Name")),)
    def __unicode__(self):
        return self.label(lang=get_language())

class Talk(models.Model):
    YES_NO = ((1,_(u"Yes")),(0,_(u"No")),)
    NO_YES_MAYBE = ((0,_(u"No")),(1,_(u"Yes")),(2,_(u"I don't know yet")),)
    STATUS = ((1,_(u"Accepted")),(0,_(u"Rejected")),)
    NATURES = (('conference',_(u"Conference")),('workshop',_(u"Workshop")),)

    date = models.DateField(_(u"Send date"), auto_now=True)
    status = models.PositiveSmallIntegerField(_(u"Status"), choices=STATUS, null=True, blank=True)
    topic = models.ForeignKey(Topic)
    title = models.CharField(_(u"Title"), max_length=128)
    nature = models.CharField(_(u"Nature"), choices=NATURES, max_length=24, blank=True)
    abstract = models.TextField(_(u"Abstract"))
    language = models.ForeignKey(Language)
    capture = models.PositiveSmallIntegerField(u"Capture", choices=YES_NO)
    license = models.ForeignKey(License, null=True, blank=True)
    constraints = models.TextField(_(u"Constraints"), blank=True)
    speakers = models.TextField(_(u"Speaker(s)"))
    biography = models.TextField(_(u"Biography"))
    charges = models.PositiveSmallIntegerField(_(u"Refund charges"), choices=NO_YES_MAYBE, blank=True)
    city = models.CharField(_(u"City"), max_length=128, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    transportation = models.ForeignKey(Transportation, null=True, blank=True)
    cost = models.CharField(_(u"Estimated cost"), max_length=64, blank=True)
    notes = models.TextField(_(u"Notes"), blank=True)

    def save(self):
        super(Talk, self).save()
        talk = Talk.objects.get(id=self.id)
        tmpl = loader.get_template('manager/summary_mail.txt')
        ctx = {'talk': talk}
        subject = _(u"[RMLL/LSM] [Topic: %s] New talk") % talk.topic.label()
        send_mail(subject, tmpl.render(Context(ctx)), settings.CFP_NOTICE_FROM_EMAIL, [talk.topic.email])
        mail_admins(subject, tmpl.render(Context(ctx)))
