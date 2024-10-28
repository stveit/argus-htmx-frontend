from django import forms
from django.forms import ModelForm

from argus.notificationprofile.models import DestinationConfig
from .utils import _get_settings_key_for_media


class DestinationFormCreate(ModelForm):
    settings = forms.CharField(required=True)

    class Meta:
        model = DestinationConfig
        fields = ["label", "media", "settings"]
        labels = {
            "label": "Name",
        }

    def clean(self):
        super().clean()
        settings_key = _get_settings_key_for_media(self.cleaned_data["media"])
        self.cleaned_data["settings"] = {settings_key: self.cleaned_data["settings"]}
        return self.cleaned_data


class DestinationFormUpdate(ModelForm):
    value = forms.CharField(required=True)

    class Meta:
        model = DestinationConfig
        fields = ["label"]
        labels = {
            "label": "Name",
        }
