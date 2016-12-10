from django.contrib import messages
from django.shortcuts import redirect, render

from core.localization.messages import MSG_PASSWORDS_UNEQUAL, MSG_SETTINGS_SAVED, MSG_OFM_PASSWORDS_UNEQUAL, \
    MSG_NOT_LOGGED_IN
from users.models import OFMUser


def _handle_account_data_change(request, email, password, password2):
    if email:
        if OFMUser.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Ein anderer Account existiert bereits mit dieser E-Mail-Adresse.")
            return
        request.user.email = email
    if password and password2:
        if password != password2:
            messages.error(request, MSG_PASSWORDS_UNEQUAL)
            return
        request.user.set_password(password)
    request.user.save()
    messages.success(request, MSG_SETTINGS_SAVED)


def _handle_ofm_data_change(request, ofm_password, ofm_password2):
    if ofm_password != ofm_password2:
        messages.error(request, MSG_OFM_PASSWORDS_UNEQUAL)
        return redirect('core:register')

    request.user.ofm_password = ofm_password
    request.user.save()
    messages.success(request, MSG_SETTINGS_SAVED)


def settings_view(request):
    if request.user.is_authenticated():
        if request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            ofm_password = request.POST.get('ofm_password')
            ofm_password2 = request.POST.get('ofm_password2')

            if email or (password and password2):
                _handle_account_data_change(request, email, password, password2)
            elif ofm_password and ofm_password2:
                _handle_ofm_data_change(request, ofm_password, ofm_password2)
            else:
                messages.error(request, "Die Daten waren nicht vollständig. Bitte überprüfe die Eingabe.")

        return render(request, 'core/account/settings.html')
    else:
        messages.error(request, MSG_NOT_LOGGED_IN)
        return redirect('core:login')
