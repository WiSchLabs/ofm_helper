from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms.registration_form import RegistrationForm
from core.localization.messages import PASSWORDS_UNEQUAL, OFM_PASSWORDS_UNEQUAL, NOT_LOGGED_IN, \
    OFM_USERNAME_ALREADY_EXISTS, USERNAME_ALREADY_EXISTS, EMAIL_ALREADY_EXISTS, ALREADY_LOGGED_IN, \
    ACCOUNT_CREATED, LOGGED_OUT, USERNAME_OR_PASSWORD_INVALID, LOGIN_IMPOSSIBLE_ACCOUNT_IS_DEACTIVATED, \
    LOGIN_SUCCESSFUL
from users.models import OFMUser


class OFMUserCreate(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('core:account:login')
    template_name = 'core/account/register.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            messages.error(self.request, ALREADY_LOGGED_IN)
            return render(self.request, 'core/account/home.html')

        if self.is_registration_form_invalid(form):
            return super(OFMUserCreate, self).form_invalid(form)

        messages.success(self.request, ACCOUNT_CREATED)
        return super(OFMUserCreate, self).form_valid(form)

    def is_registration_form_invalid(self, form):
        form_invalid = False
        if OFMUser.objects.filter(username=form.data['username']).exists():
            messages.error(self.request, USERNAME_ALREADY_EXISTS)
            form_invalid = True
        if OFMUser.objects.filter(email=form.data['email']).exists():
            messages.error(self.request, EMAIL_ALREADY_EXISTS)
            form_invalid = True
        if form.data['password'] != form.data['password2']:
            messages.error(self.request, PASSWORDS_UNEQUAL)
            form_invalid = True
        if OFMUser.objects.filter(ofm_username=form.data['ofm_username']).exists():
            messages.error(self.request, OFM_USERNAME_ALREADY_EXISTS)
            form_invalid = True
        if form.data['ofm_password'] != form.data['ofm_password2']:
            messages.error(self.request, OFM_PASSWORDS_UNEQUAL)
            form_invalid = True
        return form_invalid


def login_view(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, LOGIN_SUCCESSFUL)
                return render(request, 'core/account/home.html')
            else:
                messages.error(request, LOGIN_IMPOSSIBLE_ACCOUNT_IS_DEACTIVATED)
                return redirect('core:account:login')
        else:
            messages.error(request, USERNAME_OR_PASSWORD_INVALID)
            return redirect('core:account:login')
    else:
        if request.user.is_authenticated():
            return render(request, 'core/account/home.html')
        else:
            return render(request, 'core/account/login.html')


def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        messages.success(request, LOGGED_OUT)
    return redirect('core:home')


def account_view(request):
    if request.user.is_authenticated():
        return render(request, 'core/account/home.html')
    else:
        messages.error(request, NOT_LOGGED_IN)
        return redirect('core:account:login')
