from django import forms
from django.forms import ModelForm

from argus.notificationprofile.models import DestinationConfig


class DestinationFormCreate(ModelForm):
    value = forms.CharField(required=True)

    class Meta:
        model = DestinationConfig
        fields = ["label", "media"]


class DestinationFormUpdate(ModelForm):
    value = forms.CharField(required=True)

    class Meta:
        model = DestinationConfig
        fields = ["label"]
