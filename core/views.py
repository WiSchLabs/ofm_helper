from bs4 import BeautifulSoup

from core.parsers.finances_parser import FinancesParser
from core.parsers.match_parser import MatchParser
from core.parsers.matchday_parser import MatchdayParser
from core.parsers.won_by_default_match_parser import WonByDefaultMatchParser
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.parsers.players_parser import PlayersParser
from core.parsers.stadium_stand_statistics_parser import StadiumStandStatisticsParser
from core.parsers.stadium_statistics_parser import StadiumStatisticsParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from users.models import OFMUser
import logging

logger = logging.getLogger(__name__)


def register_view(request):
    if request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, "You are already logged in. You can logout from the side menu.",
                             extra_tags="error")
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
            messages.add_message(request, messages.ERROR, "An account with this email address already exists",
                                 extra_tags="error")
            return redirect('core:register')

        if OFMUser.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "An account with this username already exists",
                                 extra_tags="error")
            return redirect('core:register')

        if password != password2:
            messages.add_message(request, messages.ERROR, "Your passwords don't match!",
                                 extra_tags="error")
            return redirect('core:register')

        if OFMUser.objects.filter(ofm_username=ofm_username).exists():
            messages.add_message(request, messages.ERROR, "There is already an account linked to this OFM username",
                                 extra_tags="error")
            return redirect('core:register')

        if ofm_password != ofm_password2:
            messages.add_message(request, messages.ERROR, "Your OFM passwords don't match!",
                                 extra_tags="error")
            return redirect('core:register')

        OFMUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            ofm_username=ofm_username,
            ofm_password=ofm_password,
        )

        messages.add_message(request, messages.SUCCESS, "Account created. Please log in.", extra_tags="success")
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
                messages.add_message(request, messages.SUCCESS, "Login successful.", extra_tags='success')
                return render(request, 'core/account/home.html')
            else:
                messages.add_message(request, messages.ERROR, "Your account is disabled.", extra_tags='danger')
                return redirect('core:login')
        else:
            messages.add_message(request, messages.ERROR, "Your username and/or your password is incorrect.",
                                 extra_tags='warning')
            return redirect('core:login')
    else:
        if request.user.is_authenticated():
            return render(request, 'core/account/home.html')
        else:
            return render(request, 'core/account/login.html')


def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        messages.add_message(request, messages.SUCCESS, "You have been logged out.", extra_tags='success')
    return redirect('core:home')


def account_view(request):
    if request.user.is_authenticated():
        return render(request, 'core/account/home.html')
    else:
        messages.add_message(request, messages.ERROR, "You are not logged in!", extra_tags='error')
        return redirect('core:login')


def trigger_parsing(request):
    logger.debug('===== START parsing ==============================')
    if request.user.is_authenticated():
        logger.debug('===== got user: %s' % request.user.username)
        logger.debug('===== SiteManager login ...')
        site_manager = SiteManager(request.user)
        site_manager.login()

        parse_matchday(site_manager)
        parse_players(request, site_manager)
        parse_player_statistics(request, site_manager)
        parse_finances(request, site_manager)
        parse_match(request, site_manager)

        site_manager.kill()
        logger.debug('===== END parsing ==============================')

        return redirect('core:ofm:player_statistics')
    else:
        messages.add_message(request, messages.ERROR, "You are not logged in!", extra_tags='error')
        return redirect('core:login')


def parse_matchday(site_manager):
    logger.debug('===== parse Matchday ...')
    site_manager.jump_to_frame(Constants.HEAD)
    matchday_parser = MatchdayParser(site_manager.browser.page_source)
    matchday_parser.parse()


def parse_players(request, site_manager):
    logger.debug('===== parse Players ...')
    site_manager.jump_to_frame(Constants.TEAM.PLAYERS)
    players_parser = PlayersParser(site_manager.browser.page_source, request.user)
    players_parser.parse()


def parse_player_statistics(request, site_manager):
    logger.debug('===== parse PlayerStatistics ...')
    site_manager.jump_to_frame(Constants.TEAM.PLAYER_STATISTICS)
    player_stat_parser = PlayerStatisticsParser(site_manager.browser.page_source, request.user)
    player_stat_parser.parse()


def parse_finances(request, site_manager):
    logger.debug('===== parse Finances ...')
    site_manager.jump_to_frame(Constants.FINANCES.OVERVIEW)
    finances_parser = FinancesParser(site_manager.browser.page_source, request.user)
    finances_parser.parse()


def parse_match(request, site_manager):
    logger.debug('===== parse latest Match ...')
    site_manager.jump_to_frame(Constants.LEAGUE.MATCHDAY_TABLE)
    soup = BeautifulSoup(site_manager.browser.page_source, "html.parser")
    row = soup.find(id='table_head').find_all('b')[0].find_parent('tr')
    is_home_match = "<b>" in str(row.find_all('td')[2].a)
    match_report_image = row.find_all('img', class_='changeMatchReportImg')
    if match_report_image:
        link_to_match = match_report_image[0].find_parent('a')['href']
        if "spielbericht" in link_to_match:
            site_manager.jump_to_frame(Constants.BASE + link_to_match)
            match_parser = MatchParser(site_manager.browser.page_source, request.user, is_home_match)
            match_parser.parse()

            if is_home_match:
                parse_stadium_statistics(request, site_manager)
    else:
        match_parser = WonByDefaultMatchParser(site_manager.browser.page_source, request.user)
        match_parser.parse()


def parse_stadium_statistics(request, site_manager):
    logger.debug('===== parse latest Stadium statistics ...')
    site_manager.jump_to_frame(Constants.STADIUM.ENVIRONMENT)
    stadium_statistics_parser = StadiumStatisticsParser(site_manager.browser.page_source, request.user)
    stadium_statistics_parser.parse()
    site_manager.jump_to_frame(Constants.STADIUM.OVERVIEW)
    stadium_stand_stat_parser = StadiumStandStatisticsParser(site_manager.browser.page_source, request.user)
    stadium_stand_stat_parser.parse()
