from braces.views import CsrfExemptMixin
from braces.views import JSONResponseMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.localization.messages import PASSWORDS_UNEQUAL, SETTINGS_SAVED, OFM_PASSWORDS_UNEQUAL, NOT_LOGGED_IN
from core.models import ParsingSetting
from users.models import OFMUser


def _handle_account_data_change(request, email, password, password2):
    if email:
        if OFMUser.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Ein anderer Account existiert bereits mit dieser E-Mail-Adresse.")
            return
        request.user.email = email
    if password and password2:
        if password != password2:
            messages.error(request, PASSWORDS_UNEQUAL)
            return
        request.user.set_password(password)
    request.user.save()
    messages.success(request, SETTINGS_SAVED)


def _handle_ofm_data_change(request, ofm_password, ofm_password2):
    if ofm_password != ofm_password2:
        messages.error(request, OFM_PASSWORDS_UNEQUAL)
        return redirect('core:account:settings')

    request.user.ofm_password = ofm_password
    request.user.save()
    messages.success(request, SETTINGS_SAVED)


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
        messages.error(request, NOT_LOGGED_IN)
        return redirect('core:account:login')


@method_decorator(login_required, name='dispatch')
class GetParsingSettingsView(JSONResponseMixin, View):
    def get(self, request):
        parsing_setting, _ = ParsingSetting.objects.get_or_create(user=request.user)

        settings_dict = dict()
        settings_dict['parsing_player_statistics'] = parsing_setting.parsing_chain_includes_player_statistics
        settings_dict['parsing_awp_boundaries'] = parsing_setting.parsing_chain_includes_awp_boundaries
        settings_dict['parsing_finances'] = parsing_setting.parsing_chain_includes_finances
        settings_dict['parsing_matches'] = parsing_setting.parsing_chain_includes_matches
        settings_dict['parsing_match_details'] = parsing_setting.parsing_chain_includes_match_details
        settings_dict['parsing_match_details_only_for_current_matchday'] = \
            parsing_setting.parsing_chain_includes_match_details_only_for_current_matchday
        settings_dict['parsing_stadium_details'] = parsing_setting.parsing_chain_includes_stadium_details

        return self.render_json_response(settings_dict)


@method_decorator(login_required, name='dispatch')
class UpdateParsingSettingItemStatusView(CsrfExemptMixin, JSONResponseMixin, View):
    def post(self, request):
        parsing_setting, _ = ParsingSetting.objects.get_or_create(user=request.user)

        parsing_player_statistics = self._validate_boolean(
                request.POST.get('parsing_player_statistics',
                                 default=parsing_setting.parsing_chain_includes_player_statistics))
        parsing_awp_boundaries = self._validate_boolean(
                request.POST.get('parsing_awp_boundaries',
                                 default=parsing_setting.parsing_chain_includes_awp_boundaries))
        parsing_finances = self._validate_boolean(
                request.POST.get('parsing_finances',
                                 default=parsing_setting.parsing_chain_includes_finances))
        parsing_matches = self._validate_boolean(
                request.POST.get('parsing_matches',
                                 default=parsing_setting.parsing_chain_includes_matches))
        parsing_match_details = self._validate_boolean(
                request.POST.get('parsing_match_details',
                                 default=parsing_setting.parsing_chain_includes_match_details))
        parsing_match_details_only_for_current_matchday = self._validate_boolean(
                request.POST.get('parsing_match_details_only_for_current_matchday',
                                 default=parsing_setting.parsing_chain_includes_match_details_only_for_current_matchday)
        )
        parsing_stadium_details = self._validate_boolean(
                request.POST.get('parsing_stadium_details',
                                 default=parsing_setting.parsing_chain_includes_stadium_details))

        if not parsing_matches:
            parsing_match_details = False
            parsing_stadium_details = False

        if not parsing_match_details:
            parsing_match_details_only_for_current_matchday = False
            parsing_stadium_details = False

        parsing_setting.parsing_chain_includes_player_statistics = parsing_player_statistics
        parsing_setting.parsing_chain_includes_awp_boundaries = parsing_awp_boundaries
        parsing_setting.parsing_chain_includes_finances = parsing_finances
        parsing_setting.parsing_chain_includes_matches = parsing_matches
        parsing_setting.parsing_chain_includes_match_details = parsing_match_details
        parsing_setting.parsing_chain_includes_match_details_only_for_current_matchday = \
            parsing_match_details_only_for_current_matchday
        parsing_setting.parsing_chain_includes_stadium_details = parsing_stadium_details
        parsing_setting.save()

        return self.render_json_response({'success': True})

    @staticmethod
    def _validate_boolean(value):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            return value
