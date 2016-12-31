from django.forms import ModelForm

from users.models import OFMUser


class RegistrationForm(ModelForm):
    class Meta:
        model = OFMUser
        fields = ['username', 'password', 'email', 'ofm_username', 'ofm_password']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        user.ofm_username = self.cleaned_data['ofm_username']
        user.ofm_password = self.cleaned_data['ofm_password']

        if commit:
            user.save()
