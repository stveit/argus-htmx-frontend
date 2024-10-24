from django import forms

from argus.notificationprofile.models import Media


class DestinationForm(forms.Form):
    label = forms.CharField(required=False)
    media = forms.ChoiceField(choices=[(m.slug, m.name) for m in Media.objects.all()])
    value = forms.CharField(required=True)
