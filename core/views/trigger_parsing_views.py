import os
import subprocess
from django.contrib import messages
from django.shortcuts import redirect

from core.localization.messages import NOT_LOGGED_IN, NEWER_OFM_VERSION_AVAILABLE
from core.managers.parser_manager import ParserManager
from core.managers.site_manager import OFMSiteManager, OFMTransferSiteManager
from core.models import Matchday
from ofm_helper.common_settings import BASE_DIR


def trigger_parsing(request):
    if request.user.is_authenticated():
        site_manager = OFMSiteManager(request.user)
        site_manager.login()

        pm = ParserManager()
        pm.parse_all_ofm_data(site_manager)

        remote_version = pm.parse_ofm_version(site_manager)
        try:
            with open('version', 'r') as version_file:
                own_version = version_file.read().replace('\n', '')
            if own_version != "null" and own_version != remote_version:
                messages.info(request, NEWER_OFM_VERSION_AVAILABLE % (remote_version, own_version))
        except IOError:
            pass

        site_manager.kill_browser()

        return redirect('core:ofm:player_statistics')
    else:
        messages.error(request, NOT_LOGGED_IN)
        return redirect('core:account:login')


def trigger_single_parsing(request, parsing_function, redirect_to='core:account:home'):
    if request.user.is_authenticated():
        site_manager = OFMSiteManager(request.user)
        site_manager.login()
        parsing_function(site_manager)
        return redirect(redirect_to)
    else:
        messages.error(request, NOT_LOGGED_IN)
        return redirect('core:account:login')


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


def trigger_transfer_download(request):
    matchday = request.GET.get("matchday")
    current_matchday = Matchday.get_current()

    filtered_matchdays = Matchday.objects.filter(season__number=current_matchday.season.number,
                                                 number=matchday if matchday else current_matchday.number)
    if len(filtered_matchdays) == 1:
        matchday = filtered_matchdays[0]
    else:
        matchday = current_matchday

    site_manager = OFMTransferSiteManager(request.user)
    site_manager.download_transfer_excel(matchday)
    site_manager.kill_browser()

    data_folder = os.path.join(BASE_DIR, 'ofm_transfer_data')
    script_file = os.path.join(data_folder, 'convert_xls_to_csv.sh')
    subprocess.call([script_file], cwd=data_folder)

    return redirect('core:ofm:transfers')
