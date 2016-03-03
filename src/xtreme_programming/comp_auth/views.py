import datetime

from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import redirect, render_to_response, render

from .forms import LoginForm
from .settings import COMPETITION_TOKEN


def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['competition_token'] == COMPETITION_TOKEN:
                if _still_available(form.cleaned_data['team_token']):
                    team_token = form.cleaned_data['team_token']
                    user = User.objects.filter(team__token=team_token)[0]
                    team = user.team
                    # user = authenticate(username=team.name + "_user")
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    return redirect('/wait')
    form = LoginForm()

    if settings.DEBUG:
        users = User.objects.all()
        token = COMPETITION_TOKEN
    else:
        users = None
        token = None

    return render(request,
                  'comp_auth/login.html',
                  context={"users_list": users,
                           "token": token,
                           "form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login'))


def _still_available(team_token):
    spots_left = settings.MAX_USERS_PER_TEAM
    sessions = Session.objects.filter(
        expire_date__gte=datetime.datetime.now()
    )
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    users = User.objects.filter(id__in=uid_list)

    if spots_left > 0:
        for user in users:
            if user.is_superuser:
                continue
            elif user.team.token == team_token:
                spots_left -= 1

    return spots_left > 0


