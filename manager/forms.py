# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from models import Topic, TopicLabel, Language, LanguageLabel, Country, CountryLabel, Transportation, TransportationLabel, Talk, License

# construction dynamique des classes de formulaires
bases = (forms.ModelForm,)


def base__init__(self, *args, **keys):
    """
    Alimentation du formulaire en modification
    """
    if 'instance' in keys and keys['instance']:
        instance = keys['instance']
        property_dct = {}
        if self.label_model:
            labels = self.label_model.objects.filter(parent=instance)
            for label in labels:
                property_dct['label_%s_%d' % (label.language, label.label_number)] = label.value
        if 'initial' in keys:
            keys['initial'].update(property_dct)
        else:
            keys['initial'] = property_dct
    forms.ModelForm.__init__(self, *args, **keys)


def base_save(self, *args, **keys):
    """
    Sauvegarde du formulaire avec prise en compte du champ libellé
    """
    new_obj = forms.ModelForm.save(self, *args, **keys)
    new_obj.save()

    def save_labels(self, label_model, nb_labels, extra_id=''):
        if not label_model:
            return
        labels = label_model.objects.filter(parent=new_obj)
        old_languages = []
        for label in labels:
            if label.label_number >= nb_labels:
                label.delete()
                label.save()
                continue
            lbl = self.cleaned_data[extra_id + 'label_%s_%d' % (label.language,
                                                                label.label_number)]
            old_languages.append((label.language, label.label_number))
            label.value = lbl
            label.save()
        # initialisation des labels non présents en base
        for idx in xrange(nb_labels):
            for language_id, language_label in settings.LANGUAGES:
                if (language_id, idx) not in old_languages:
                    lbl = self.cleaned_data[extra_id + 'label_%s_%d' % (language_id, idx)]
                    label_model.objects.create(parent=new_obj, value=lbl,
                                               language=language_id, label_number=idx)

    save_labels(self, self.label_model, self.nb_labels)
    return new_obj


def get_attributes(base_class):
    labels = base_class.labels
    atts = {'nb_labels': len(labels)}
    for idx in xrange(len(labels)):
        for language_id, language_label in settings.LANGUAGES:
            atts['label_%s_%d' % (language_id, idx)] = \
                forms.CharField(label=labels[idx][1] + u" (%s)" % language_label,
                                widget=forms.TextInput, required=False, max_length=256)
    atts['__init__'] = base__init__
    atts['save'] = base_save
    return atts


TopicAdminFormBase = getattr(forms.ModelForm, '__metaclass__', type) \
                            ('TopicAdminFormBase', bases, get_attributes(Topic))


class TopicAdminForm(TopicAdminFormBase):
    label_model = TopicLabel

    class Meta:
        model = Topic

LanguageAdminFormBase = getattr(forms.ModelForm, '__metaclass__', type) \
    ('LanguageAdminFormBase', bases, get_attributes(Language))


class LanguageAdminForm(LanguageAdminFormBase):
    label_model = LanguageLabel

    class Meta:
        model = Language

CountryAdminFormBase = getattr(forms.ModelForm, '__metaclass__', type) \
    ('CountryAdminFormBase', bases, get_attributes(Country))


class CountryAdminForm(CountryAdminFormBase):
    label_model = CountryLabel

    class Meta:
        model = Country

TransportationAdminFormBase = getattr(forms.ModelForm, '__metaclass__', type) \
    ('TransportationAdminFormBase', bases, get_attributes(Transportation))


class TransportationAdminForm(TransportationAdminFormBase):
    label_model = TransportationLabel

    class Meta:
        model = Transportation


# Ugly hack
from django.forms import widgets
from django.utils.encoding import force_unicode
from itertools import chain
from operator import itemgetter


class SortedForm(widgets.Select):
    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        values = []
        for k, v in chain(self.choices, choices):
            values.append((k, v))
        values.sort(key=itemgetter(1))
        output = []
        for option_value, option_label in values:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)

_iattrs = {'class': 'text', 'size': 60}
_tattrs = {'cols': '80', 'rows': 12}


class TalkForm(forms.ModelForm):
    language = forms.ModelChoiceField(label=_(u"Language"),
                                      queryset=Language.objects.all(), empty_label=None)
    topic = forms.ModelChoiceField(label=_(u"Topic"),
                                   queryset=Topic.objects.all(), empty_label=None, widget=SortedForm)
    title = forms.CharField(label=_(u"Title"),
                            min_length=5, widget=forms.TextInput(attrs=_iattrs))
    nature = forms.ChoiceField(label=_(u"Type"), choices=Talk.NATURES, required=True)
    abstract = forms.CharField(label=_(u"Summary"), widget=forms.Textarea(attrs=_tattrs),
                               help_text=_(u"A description of what the talk would be about. This abstract will be published on the website."),
                               )
    abstract_other_language = forms.CharField(label=_(u"Summary in French"), widget=forms.Textarea(attrs=_tattrs),
                                              help_text=_(u"Same but in French. If you don't know French, don't worry, we'll handle this for you."),
                                             )
    capture = forms.ChoiceField(label=_(u"Capture"), choices=Talk.YES_NO, required=False,
                                help_text=_(u"Choose “yes” if the speaker(s) agree for the talk to be captured (audio and/or video) and published on the event website (and probably spread on the whole Internet)."),
                                )
    license = forms.ModelChoiceField(label=_(u"License"),
                                     required=False, queryset=License.objects.all(),
                                     help_text=_(u"The preferred license for the capture of the talk (contact us if you want us to add another license)."),
                                     )
    constraints = forms.CharField(label=_(u"Constraints"),
                                  widget=forms.Textarea(attrs=_tattrs), required=False,
                                  help_text=_(u"If the speaker(s) have special needs, constraints (be scheduled on a specific date, disabled person moving with a wheelchair, etc) or something else."),
                                  )

    for_general_public = forms.BooleanField(label=_(u"General public"))
    for_professionals = forms.BooleanField(label=_(u"Professionals"))
    for_decision_makers = forms.BooleanField(label=_(u"Decision makers"))
    for_geeks = forms.BooleanField(label=_(u"Geeks"))
    for_english_speaking_people = forms.BooleanField(label=_(u"English speaking people"))

    speakers = forms.CharField(label=_(u"Speaker(s)"), widget=forms.Textarea(attrs=_tattrs),
                               help_text=_(u"First name, last name, email of the speaker(s). One speaker per line. Each line should respect the following format: « Firstname Lastname [speaker@domain.tld] »"),
                               )
    biography = forms.CharField(label=_(u"Biography"), widget=forms.Textarea(attrs=_tattrs),
                                help_text=_(u"Add a few words about the speaker(s). Their, work, activities, involvement in free software, etc. It will be published with the abstract on the event website."),
                                )
    biography_other_language = forms.CharField(label=_(u"Biography in French"), widget=forms.Textarea(attrs=_tattrs),
                                help_text=_(u"Same but in French. If you don't know French, don't worry, we'll handle this for you."),
                                )
    charges = forms.ChoiceField(label=(_(u"Refund charges")),
                                choices=Talk.NO_YES_MAYBE, required=False)
    transportation = forms.ModelChoiceField(label=_(u"Transportation"),
                                            queryset=Transportation.objects.all(), required=False)
    city = forms.CharField(label=_(u"City"), min_length=3,
                           required=False, widget=forms.TextInput(attrs=_iattrs))
    country = forms.ModelChoiceField(label=_(u"Country"), widget=SortedForm,
                                     required=False, queryset=Country.objects.all())
    cost = forms.CharField(label=_(u"Estimated cost (euros)"),
                           required=False, widget=forms.TextInput(attrs=_iattrs),
                           help_text=_(u"If you know the estimated cost of the transportation, it will be easier for us to have a clear view of the expenses we could engage."),
                           )

    class Meta:
        model = Talk
        exclude = ('status', 'notes')

    def clean(self):
        cleaned_data = self.cleaned_data
        capture = cleaned_data.get('capture')
        license = cleaned_data.get('license')
        charges = cleaned_data.get('charges')
        city = cleaned_data.get('city')
        country = cleaned_data.get('country')
        speakers = cleaned_data.get('speakers')

        if capture == '1' and license == None:
            self._errors['license'] = self.error_class([_(u"This field is required.")])
            del cleaned_data['license']

        if charges != '0':
            if city == '':
                self._errors['city'] = self.error_class([_(u"This field is required.")])
                del cleaned_data['city']
            if country == None:
                self._errors['country'] = self.error_class([_(u"This field is required.")])
                del cleaned_data['country']

        if speakers != None:
            if speakers.strip() == '':
                self._errors['speakers'] = self.error_class([_(u"This field is required.")])
            else:
                speaker_re = Talk.speaker_re()

                speakers = speakers.strip()
                errors = []
                success = []
                for s in speakers.split("\n"):
                    s = s.strip()
                    if speaker_re.match(s) == None:
                        errors.append(s)
                    else:
                        success.append(s)

                if errors != []:
                    errors.reverse()
                    errors.append(_(u"The following lines don't match the correct format:"))
                    errors.reverse()
                    self._errors['speakers'] = self.error_class(errors)
                    del cleaned_data['speakers']

        return cleaned_data


class TalkAdminForm(TalkForm):

    notes = forms.CharField(label=_(u"Notes"),
                            required=False, widget=forms.Textarea(attrs=_tattrs))

    class Meta:
        exclude = ()
