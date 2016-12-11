from django.contrib import messages
from django.shortcuts import redirect

from core.localization.messages import NOT_LOGGED_IN, NEWER_OFM_VERSION_AVAILABLE
from core.managers.parser_manager import ParserManager
from core.managers.site_manager import SiteManager


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
                messages.info(request, NEWER_OFM_VERSION_AVAILABLE % (remote_version, own_version))
        except IOError:
            pass

        site_manager.kill()

        return redirect('core:ofm:player_statistics')
    else:
        messages.error(request, NOT_LOGGED_IN)
        return redirect('core:login')


def trigger_single_parsing(request, parsing_function, redirect_to='core:account'):
    if request.user.is_authenticated():
        site_manager = SiteManager(request.user)
        site_manager.login()
        parsing_function(request, site_manager)
        return redirect(redirect_to)
    else:
        messages.error(request, NOT_LOGGED_IN)
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
