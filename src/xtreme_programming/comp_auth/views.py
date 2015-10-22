import datetime

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import redirect, render_to_response

from .forms import LoginForm


# Create your views here.
def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        render_to_response('comp_auth/login.html', context={"form": form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if _still_available(form.team_token):
                login(request)
                redirect('competition.index')


def logout_view(request):
    logout(request)
    redirect('login_view')


def _still_available(team_token):
    spots_left = settings.MAX_USERS_PER_TEAM
    sessions = Session.objects.filter(
        expire_date_time__gte=datetime.datetime.now()
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
            if user.participant.team.token == team_token:
                spots_left -= 1

    return spots_left > 0


