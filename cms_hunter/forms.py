from .models import Scanning
from django import forms


class SearchHosts(forms.Form):
    search = forms.CharField(max_length=100, label="", required=False)


class ScanForm(forms.Form):
    INTENSIVE_CHOICE = (("1", "Light"), ("3", "Medium"), ("4", "Aggressive"))

    PROXY_TYPES = (
        ('http', 'http'),
        ('https', 'https'),
    )

    hostname = forms.CharField(max_length=100)
    intensive = forms.ChoiceField(choices=INTENSIVE_CHOICE, required=False)

    proxy_server = forms.BooleanField(required=False)
    ip = forms.GenericIPAddressField(required=False)
    port = forms.IntegerField(required=False)
    proxy_type = forms.ChoiceField(choices=PROXY_TYPES, required=False)
    socks = forms.BooleanField(required=False)
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, required=False)


class VulnerabilityScanForm(forms.ModelForm):
    PROXY_TYPES = (
        ('http', 'http'),
        ('https', 'https'),
    )

    webserver = forms.BooleanField(required=False)
    ip = forms.BooleanField(required=False)
    country = forms.BooleanField(required=False)
    cms = forms.BooleanField(required=False)

    proxy_server = forms.BooleanField(required=False)
    proxy_ip = forms.GenericIPAddressField(required=False)
    port = forms.IntegerField(required=False)
    proxy_type = forms.ChoiceField(choices=PROXY_TYPES, required=False)
    socks = forms.BooleanField(required=False)
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, required=False)

    class Meta:
        model = Scanning
        exclude = ('hostname', "status", "message")
