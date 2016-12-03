from braces.views import CsrfExemptMixin
from braces.views import JsonRequestResponseMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from core.managers.parser_manager import ParserManager
from core.managers.site_manager import SiteManager
from core.models import ChecklistItem, Checklist, Matchday, Match
from users.models import OFMUser

MSG_NOT_LOGGED_IN = "Du bist nicht eingeloggt!"
MSG_SETTINGS_SAVED = "Die neuen Einstellungen wurden gespeichert."
MSG_PASSWORDS_UNEQUAL = "Die eingegeben Passwörter stimmen nicht überein."
MSG_OFM_PASSWORDS_UNEQUAL = "Die eingegeben OFM Passwörter stimmen nicht überein."


def register_view(request):
    if request.user.is_authenticated():
        messages.error(request, "Du bist bereits eingeloggt. Du kannst dich im Menü ausloggen.")
        return render(request, 'core/account/home.html')
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        ofm_username = request.POST.get('ofm_username')
        ofm_password = request.POST.get('ofm_password')
        ofm_password2 = request.POST.get('ofm_password2')

        if OFMUser.objects.filter(email=email).exists():
            messages.error(request, "Ein Account mit dieser E-Mail-Adresse existiert bereits.")
            return redirect('core:register')

        if OFMUser.objects.filter(username=username).exists():
            messages.error(request, "Ein Account mit diesem Benutzernamen existiert bereits.")
            return redirect('core:register')

        if password != password2:
            messages.error(request, MSG_PASSWORDS_UNEQUAL)
            return redirect('core:register')

        if OFMUser.objects.filter(ofm_username=ofm_username).exists():
            messages.error(request, "Es existiert bereits ein Account für diesen OFM Benutzernamen.")
            return redirect('core:register')

        if ofm_password != ofm_password2:
            messages.error(request, MSG_OFM_PASSWORDS_UNEQUAL)
            return redirect('core:register')

        OFMUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            ofm_username=ofm_username,
            ofm_password=ofm_password,
        )

        messages.success(request, "Account wurde erstellt. Jetzt kannst du dich einloggen.")
        return redirect('core:login')

    else:
        return render(request, 'core/account/register.html')


def login_view(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Login erfolgreich.")
                return render(request, 'core/account/home.html')
            else:
                messages.error(request, "Login nicht möglich. Dein Account wurde deaktiviert.")
                return redirect('core:login')
        else:
            messages.error(request, "Benutzername und/oder Passwort nicht korrekt.")
            return redirect('core:login')
    else:
        if request.user.is_authenticated():
            return render(request, 'core/account/home.html')
        else:
            return render(request, 'core/account/login.html')


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


@method_decorator(login_required, name='dispatch')
class GetCurrentMatchdayView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        current_matchday = Matchday.get_current()
        matchday_json = dict()
        matchday_json['matchday_number'] = current_matchday.number
        matchday_json['season_number'] = current_matchday.season.number
        return self.render_json_response(matchday_json)


@method_decorator(login_required, name='dispatch')
class GetChecklistItemsView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        checklist_items = ChecklistItem.objects.filter(checklist__user=request.user)

        checklist_items_json = [_get_checklist_item_in_json(item) for item in checklist_items]

        return self.render_json_response(checklist_items_json)


@method_decorator(login_required, name='dispatch')
class GetChecklistItemsForTodayView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        current_matchday = Matchday.get_current()
        next_matchday_number = current_matchday.number + 1
        home_match_tomorrow = Match.objects.filter(
            user=request.user,
            matchday__season__number=current_matchday.season.number,
            matchday__number=next_matchday_number,
            is_home_match=True
        )
        checklist_items = ChecklistItem.objects.filter(checklist__user=request.user)
        checklist_items_everyday = checklist_items.filter(
            to_be_checked_on_matchdays=None,
            to_be_checked_on_matchday_pattern=None,
            to_be_checked_if_home_match_tomorrow=False
        )
        filtered_checklist_items = []
        filtered_checklist_items.extend(checklist_items_everyday)
        checklist_items_this_matchday = checklist_items.filter(
            to_be_checked_on_matchdays__isnull=False,
            to_be_checked_on_matchday_pattern=None,
            to_be_checked_if_home_match_tomorrow=False
        )
        filtered_checklist_items.extend([c for c in checklist_items_this_matchday if current_matchday.number in [int(x) for x in c.to_be_checked_on_matchdays.split(',')]])
        if home_match_tomorrow:
            checklist_items_home_match = checklist_items.filter(
                to_be_checked_on_matchdays=None,
                to_be_checked_on_matchday_pattern=None,
                to_be_checked_if_home_match_tomorrow=True
            )
            filtered_checklist_items.extend(checklist_items_home_match)
        if current_matchday.number > 0:
            checklist_items_matchday_pattern_pre = checklist_items.filter(
                to_be_checked_on_matchdays=None,
                to_be_checked_on_matchday_pattern__isnull=False,
                to_be_checked_if_home_match_tomorrow=False
            )
            checklist_items_matchday_pattern = [c for c
                                                in checklist_items_matchday_pattern_pre
                                                if current_matchday.number % c.to_be_checked_on_matchday_pattern == 0]
            filtered_checklist_items.extend(checklist_items_matchday_pattern)

        sorted_checklist_items = sorted(filtered_checklist_items, key=lambda x: x.priority, reverse=False)
        checklist_items_json = [_get_checklist_item_in_json(item) for item in sorted_checklist_items]

        return self.render_json_response(checklist_items_json)


def _get_checklist_item_in_json(checklist_item):
    checklist_item_json = dict()
    checklist_item_json['id'] = checklist_item.id
    checklist_item_json['name'] = checklist_item.name
    if checklist_item.to_be_checked_if_home_match_tomorrow:
        checklist_item_json['type_home_match'] = checklist_item.to_be_checked_if_home_match_tomorrow
    if checklist_item.to_be_checked_on_matchdays is not None:
        checklist_item_json['type_matchdays'] = checklist_item.to_be_checked_on_matchdays
    if checklist_item.to_be_checked_on_matchday_pattern is not None:
        checklist_item_json['type_matchday_pattern'] = checklist_item.to_be_checked_on_matchday_pattern
    checklist_item_json['checked'] = checklist_item.last_checked_on_matchday == Matchday.get_current()

    return checklist_item_json


@method_decorator(login_required, name='dispatch')
class CreateChecklistItemView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request, *args, **kwargs):
        checklist, _ = Checklist.objects.get_or_create(user=request.user)
        new_checklist_item = ChecklistItem.objects.create(checklist=checklist, name='Neuer Eintrag')

        new_checklist_item_json = _get_checklist_item_in_json(new_checklist_item)

        return self.render_json_response(new_checklist_item_json)


@method_decorator(login_required, name='dispatch')
class UpdateChecklistPriorityView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request, *args, **kwargs):
        checklist_priority = request.POST.get('checklist_priority')

        priority = [int(x) for x in checklist_priority.split(',')]
        for checklist_item_id in priority:
            checklist_item = ChecklistItem.objects.get(checklist__user=request.user, id=checklist_item_id)
            checklist_item.priority = priority.index(checklist_item_id)
            checklist_item.save()

        return self.render_json_response({'success': True})


@method_decorator(login_required, name='dispatch')
class UpdateChecklistItemView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request, *args, **kwargs):
        checklist_item_id = request.POST.get('checklist_item_id')
        checklist_item_name = request.POST.get('checklist_item_name')
        checklist_item_matchdays = request.POST.get('checklist_item_matchdays')
        checklist_item_matchday_pattern = request.POST.get('checklist_item_matchday_pattern')
        checklist_item_home_match = request.POST.get('checklist_item_home_match')
        checklist_item_everyday = request.POST.get('checklist_item_everyday')
        checklist_item_checked = request.POST.get('checklist_item_checked')

        checklist_item = ChecklistItem.objects.get(checklist__user=request.user, id=checklist_item_id)

        if checklist_item:
            if checklist_item_name:
                checklist_item.name = checklist_item_name
            elif checklist_item_matchdays:
                checklist_item.to_be_checked_on_matchdays = checklist_item_matchdays
                checklist_item.to_be_checked_on_matchday_pattern = None
                checklist_item.to_be_checked_if_home_match_tomorrow = False
            elif checklist_item_matchday_pattern:
                checklist_item.to_be_checked_on_matchdays = None
                checklist_item.to_be_checked_on_matchday_pattern = checklist_item_matchday_pattern
                checklist_item.to_be_checked_if_home_match_tomorrow = False
            elif checklist_item_home_match:
                checklist_item.to_be_checked_on_matchdays = None
                checklist_item.to_be_checked_on_matchday_pattern = None
                checklist_item.to_be_checked_if_home_match_tomorrow = True
            elif checklist_item_everyday:
                checklist_item.to_be_checked_on_matchdays = None
                checklist_item.to_be_checked_on_matchday_pattern = None
                checklist_item.to_be_checked_if_home_match_tomorrow = False
            elif checklist_item_checked == 'true':
                checklist_item.last_checked_on_matchday = Matchday.get_current()
            elif checklist_item_checked == 'false':
                checklist_item.last_checked_on_matchday = None
            checklist_item.save()
            return self.render_json_response({'success': True})
        return self.render_json_response({'success': False})


@method_decorator(login_required, name='dispatch')
class DeleteChecklistItemView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request, *args, **kwargs):
        checklist_item_id = request.POST.get('checklist_item_id')
        checklist_item = ChecklistItem.objects.get(checklist__user=request.user, id=checklist_item_id)
        if checklist_item:
            checklist_item.delete()
            return self.render_json_response({'success': True})
        return self.render_json_response({'success': False})


def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        messages.success(request, "Du wurdest abgemeldet.")
    return redirect('core:home')


def account_view(request):
    if request.user.is_authenticated():
        return render(request, 'core/account/home.html')
    else:
        messages.error(request, MSG_NOT_LOGGED_IN)
        return redirect('core:login')


def trigger_parsing(request):
    if request.user.is_authenticated():
        site_manager = SiteManager(request.user)
        site_manager.login()

        pm = ParserManager()
        pm.parse_all_ofm_data(request, site_manager)

        remote_version = pm.parse_ofm_version(site_manager)
        try:
            with open('version', 'r') as version_file:
                own_version = version_file.read().replace('\n', '')
            if own_version != "null" and own_version != remote_version:
                messages.info(request, "Es ist eine neuere Version von OFM Helper verfügbar: %s. Du nutzt noch: %s." % (remote_version, own_version))
        except IOError:
            pass

        site_manager.kill()

        return redirect('core:ofm:player_statistics')
    else:
        messages.error(request, MSG_NOT_LOGGED_IN)
        return redirect('core:login')


def trigger_single_parsing(request, parsing_function, redirect_to='core:account'):
    if request.user.is_authenticated():
        site_manager = SiteManager(request.user)
        site_manager.login()
        parsing_function(request, site_manager)
        return redirect(redirect_to)
    else:
        messages.error(request, MSG_NOT_LOGGED_IN)
        return redirect('core:login')


def trigger_matchday_parsing(request):
    pm = ParserManager()
    return trigger_single_parsing(request, pm.parse_matchday)


def trigger_players_parsing(request):
    pm = ParserManager()
    redirect_to = 'core:ofm:player_statistics'
    return trigger_single_parsing(request, pm.parse_players, redirect_to)


def trigger_player_statistics_parsing(request):
    pm = ParserManager()
    redirect_to = 'core:ofm:player_statistics'
    return trigger_single_parsing(request, pm.parse_player_statistics, redirect_to)


def trigger_finances_parsing(request):
    pm = ParserManager()
    redirect_to = 'core:ofm:finance_overview'
    return trigger_single_parsing(request, pm.parse_finances, redirect_to)


def trigger_match_parsing(request):
    pm = ParserManager()
    redirect_to = 'core:ofm:matches_overview'
    return trigger_single_parsing(request, pm.parse_all_matches, redirect_to)
