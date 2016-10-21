import logging

from bs4 import BeautifulSoup
from core.parsers.awp_boundaries_parser import AwpBoundariesParser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Matchday
from core.parsers.finances_parser import FinancesParser
from core.parsers.match_parser import MatchParser
from core.parsers.matchday_parser import MatchdayParser
from core.parsers.ofm_helper_version_parser import OfmHelperVersionParser
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.parsers.players_parser import PlayersParser
from core.parsers.stadium_stand_statistics_parser import StadiumStandStatisticsParser
from core.parsers.stadium_statistics_parser import StadiumStatisticsParser
from core.parsers.won_by_default_match_parser import WonByDefaultMatchParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from users.models import OFMUser

logger = logging.getLogger(__name__)
MSG_NOT_LOGGED_IN = "Du bist nicht eiongeloggt!"


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
    logger.debug('===== START parsing ==============================')
    if request.user.is_authenticated():
        logger.debug('===== got user: %s' % request.user.username)
        logger.debug('===== SiteManager login ...')
        site_manager = SiteManager(request.user)
        site_manager.login()

        parse_matchday(request, site_manager)
        matchday = Matchday.objects.all()[0]
        parse_players(request, site_manager)
        parse_player_statistics(request, site_manager)
        parse_awp_boundaries(request, site_manager)
        parse_finances(request, site_manager)
        if matchday.number > 0:
            #  do not parse on matchday 0
            parse_match(request, site_manager)

        remote_version = parse_ofm_version(site_manager)
        with open('.version', 'r') as version_file:
            own_version = version_file.read().replace('\n', '')
        if own_version != remote_version:
            messages.info(request, "Es ist eine neuere Version von OFM Helper verfügbar: %s. Du nutzt noch: %s." % (remote_version, own_version))

        site_manager.kill()
        logger.debug('===== END parsing ==============================')

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
    return trigger_single_parsing(request, parse_matchday)


def trigger_players_parsing(request):
    redirect_to = 'core:ofm:player_statistics'
    return trigger_single_parsing(request, parse_players, redirect_to)


def trigger_player_statistics_parsing(request):
    redirect_to = 'core:ofm:player_statistics'
    return trigger_single_parsing(request, parse_player_statistics, redirect_to)


def trigger_finances_parsing(request):
    redirect_to = 'core:ofm:finance_overview'
    return trigger_single_parsing(request, parse_finances, redirect_to)


def trigger_match_parsing(request):
    redirect_to = 'core:ofm:matches_overview'
    return trigger_single_parsing(request, parse_match, redirect_to)


def parse_ofm_version(site_manager):
    site_manager.jump_to_frame(Constants.GITHUB.LATEST_RELEASE)
    version_parser = OfmHelperVersionParser(site_manager.browser.page_source)
    return version_parser.parse()


def parse_matchday(request, site_manager):
    logger.debug('===== parse Matchday ...')
    site_manager.jump_to_frame(Constants.HEAD)
    matchday_parser = MatchdayParser(site_manager.browser.page_source)
    return matchday_parser.parse()


def parse_players(request, site_manager):
    logger.debug('===== parse Players ...')
    site_manager.jump_to_frame(Constants.TEAM.PLAYERS)
    players_parser = PlayersParser(site_manager.browser.page_source, request.user)
    return players_parser.parse()


def parse_player_statistics(request, site_manager):
    logger.debug('===== parse PlayerStatistics ...')
    site_manager.jump_to_frame(Constants.TEAM.PLAYER_STATISTICS)
    player_stat_parser = PlayerStatisticsParser(site_manager.browser.page_source, request.user)
    return player_stat_parser.parse()


def parse_awp_boundaries(request, site_manager):
    logger.debug('===== parse AWP Boundaries ...')
    site_manager.jump_to_frame(Constants.AWP_BOUNDARIES)
    awp_boundaries_parser = AwpBoundariesParser(site_manager.browser.page_source, request.user)
    awp_boundaries_parser.parse()


def parse_finances(request, site_manager):
    logger.debug('===== parse Finances ...')
    site_manager.jump_to_frame(Constants.FINANCES.OVERVIEW)
    finances_parser = FinancesParser(site_manager.browser.page_source, request.user)
    return finances_parser.parse()


def parse_match(request, site_manager):
    if Matchday.objects.all()[0].number <= 0:
        return

    logger.debug('===== parse latest Match ...')
    site_manager.jump_to_frame(Constants.LEAGUE.MATCHDAY_TABLE)
    soup = BeautifulSoup(site_manager.browser.page_source, "html.parser")
    row = soup.find(id='table_head').find_all('b')[0].find_parent('tr')
    is_home_match = "<b>" in str(row.find_all('td')[2].a)
    match_report_image = row.find_all('img', class_='changeMatchReportImg')

    if match_report_image:
        # match took place
        link_to_match = match_report_image[0].find_parent('a')['href']
        if "spielbericht" in link_to_match:
            site_manager.jump_to_frame(Constants.BASE + link_to_match)
            match_parser = MatchParser(site_manager.browser.page_source, request.user, is_home_match)
            match = match_parser.parse()

            if is_home_match:
                parse_stadium_statistics(request, site_manager)

            return match
    else:
        match_parser = WonByDefaultMatchParser(site_manager.browser.page_source, request.user)
        return match_parser.parse()


def parse_stadium_statistics(request, site_manager):
    logger.debug('===== parse latest Stadium statistics ...')
    site_manager.jump_to_frame(Constants.STADIUM.ENVIRONMENT)
    stadium_statistics_parser = StadiumStatisticsParser(site_manager.browser.page_source, request.user)
    stadium_statistics_parser.parse()
    site_manager.jump_to_frame(Constants.STADIUM.OVERVIEW)
    stadium_stand_stat_parser = StadiumStandStatisticsParser(site_manager.browser.page_source, request.user)
    return stadium_stand_stat_parser.parse()


@receiver(post_save, sender=Matchday)
def postsave(sender, **kwargs):
    pass
