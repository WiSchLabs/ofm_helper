from chartit import DataPool, Chart
from core.models import PlayerStatistics
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from users.models import OFMUser


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


def trigger_player_statistics_parsing(request):
    if request.user.is_authenticated():
        site_manager = SiteManager()
        site_manager.login()
        site_manager.jump_to_frame(Constants.TEAM.PLAYER_STATISTICS)

        player_stat_parser = PlayerStatisticsParser(site_manager.browser.page_source)
        player_stat_parser.parse()

        return redirect('core:ofm:player_statistics')
    else:
        messages.add_message(request, messages.ERROR, "You are not logged in!", extra_tags='error')
        return redirect('core:login')


def test_chart_view(request):
    # Step 1: Create a DataPool with the data we want to retrieve.
    statistics_data = \
        DataPool(
                series=
                [{'options': {
                    'source': PlayerStatistics.objects.all()},
                    'terms': [
                        'player__name',
                        'ep',
                        'tp',
                        'awp']}
                ])

    # Step 2: Create the Chart object
    chart = Chart(
            datasource=statistics_data,
            series_options=
            [{'options': {
                'type': 'column',
                'stacking': False},
                'terms': {'player__name': ['ep', 'tp', 'awp', ]}
            }],
            chart_options=
            {
                'title': {
                    'text': 'Player statistics'},
            })

    # Step 3: Send the chart object to the template.
    context = RequestContext(request)
    context['chart'] = chart

    return render_to_response('core/ofm/single_chart.html', context)
