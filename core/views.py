from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from core.managers.parser_manager import ParserManager
from core.managers.site_manager import SiteManager
from users.models import OFMUser

MSG_NOT_LOGGED_IN = "Du bist nicht eingeloggt!"


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
            messages.error(request, "Die eingegeben Passwörter stimmen nicht überein.")
            return redirect('core:register')

        if OFMUser.objects.filter(ofm_username=ofm_username).exists():
            messages.error(request, "Es existiert bereits ein Account für diesen OFM Benutzernamen.")
            return redirect('core:register')

        if ofm_password != ofm_password2:
            messages.error(request, "Die eingegeben OFM Passwörter stimmen nicht überein.")
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
        messages.add_message(request, messages.ERROR, MSG_NOT_LOGGED_IN, extra_tags='error')
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
    return trigger_single_parsing(request, pm.parse_match, redirect_to)
