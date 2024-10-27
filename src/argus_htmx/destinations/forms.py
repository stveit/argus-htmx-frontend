from django import forms
from django.forms import ModelForm

from argus.notificationprofile.models import DestinationConfig


class DestinationForm(ModelForm):
    value = forms.CharField(required=True)

    class Meta:
        model = DestinationConfig
        fields = ["label", "media"]
