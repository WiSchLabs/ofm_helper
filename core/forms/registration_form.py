from django.forms import ModelForm

from users.models import OFMUser


class RegistrationForm(ModelForm):
    class Meta:
        model = OFMUser
        fields = ['username', 'password', 'email', 'ofm_username', 'ofm_password']
