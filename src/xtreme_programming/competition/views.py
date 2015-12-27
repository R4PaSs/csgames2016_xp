import datetime
import os
import time

from random import randrange

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response

from comp_auth.models import Team

from .models import Attack, Challenge, Submission, TeamEvent
from .forms import SubmissionForm
from .yolo import yolos


NEXT_EXPIRE = None


@login_required()
def index(request):
    chals = Challenge.objects.all()

    for chal in chals:
        if chal.end:
            chal.end = int(time.mktime(chal.end.timetuple())) * 1000

    return render(request, 'competition/index.html',
                  context={'chals': chals})


@user_passes_test(lambda u: u.is_superuser)
def start(request):

    _init_cleanup()

    initial_chals = Challenge.objects.order_by('?')
    initial_chals = initial_chals[0:settings.OPEN_CHALLENGE_COUNT]

    chals = Challenge.objects.all()
    for chal in chals:
        chal.end = None
        chal.save()

    for chal in initial_chals:
        _start_challenge(chal)

    return render_to_response('competition/start.html')

@login_required()
def update(request):
    _check_open_challenges()
    data = {}
    data['chals'] = _filter_chals()
    events = _check_yolo_avail(request.user.team)
    data['yolo_avail'] = True if events else False

    current_attacks = Attack.objects.filter(receiver=request.user.team,
                                            over=False)

    if current_attacks:
        data['yolo'] = ""
        for att in current_attacks:
            attack_meta = yolos[att.attack_number]
            data['yolo'] += attack_meta['script']
            att.started = True
            att.save()

    return JsonResponse(data)

@login_required()
def problem(request, cid):
    context = {}

    if _is_open(cid):
        chal = Challenge.objects.get(pk=cid)
        context['chal'] = chal
        context['form'] = SubmissionForm(cid=cid)

    return render(request, 'competition/problem.html',
                  context=context)

@login_required()
def submit(request, cid):
    if _is_open(cid):
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            if _valid_zip(form.cleaned_data['file']):
                prev_subs = Submission.objects.filter(challenge__id=cid,
                                                      team=request.user.team)
                if not prev_subs:
                    _create_event(request.user.team)
                    _remove_attack(request.user.team)
                _save_submission(request, cid, form.cleaned_data)
                return JsonResponse({"id": cid}, status=200)

    return JsonResponse({"id": cid}, status=400)

@login_required()
def attack(request):
    team = request.user.team
    events = TeamEvent.objects.filter(team=team, used=False)
    if events:

        # Remove one Event for that team
        used_event = events[0]
        used_event.used = True
        used_event.save()

        rand_idx = randrange(0, len(yolos))
        attack_meta = yolos[rand_idx]
        if attack_meta['type'] == "distributed":
            for recv in Team.objects.all():
                atk = Attack(attacker=team,
                             receiver=recv,
                             attack_number=rand_idx)
                atk.save()
        elif attack_meta["type"] == "targeted":
            recv = randrange(0, 2)
            if recv == 0:
                recv = team
            else:
                recv = Team.objects.all().order_by('?')[0]

            atk = Attack(attacker=team,
                         receiver=recv,
                         attack_number=rand_idx)
            atk.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)


def _is_open(id):
    chal = Challenge.objects.get(pk=id)
    if chal.end:
        if chal.end > datetime.datetime.now():
            return True
    return False


def _start_challenge(chal):
    delta = datetime.timedelta(minutes=chal.length)
    chal.end = datetime.datetime.now() + delta
    chal.save()


def _init_cleanup():
    Submission.objects.all().delete()
    TeamEvent.objects.all().delete()
    Attack.objects.all().delete()


def _filter_chals():
    chals = Challenge.objects.all()
    filtered = {}
    for chal in chals:
        js_end = None
        if chal.end:
            js_end = int(time.mktime(chal.end.timetuple())) * 1000

        fchal = {
            "id": chal.id,
            "end": js_end
        }
        filtered[chal.id] = fchal

    return filtered


def _check_open_challenges():
    open_chals = Challenge.objects.filter(end__gt=datetime.datetime.now())\
        .count()
    if open_chals < settings.OPEN_CHALLENGE_COUNT:
        try:
            new_chal = Challenge.objects.filter(end__isnull=True)\
                .order_by('?')[0]
            _start_challenge(new_chal)
        except:
            pass


def _valid_zip(infile):
    return os.path.splitext(infile.name)[1] == ".zip"


def _save_submission(request, chalid, data):
    sub = Submission()
    sub.challenge_id = chalid
    sub.time = datetime.datetime.now()
    sub.comment = data['comment']
    sub.team = request.user.team

    timestr = sub.time.strftime('%H%M')
    filepath = 'submission/%s/%s/%s.zip' % \
               (sub.team.name, sub.challenge.title_EN, timestr)
    filepath = os.path.join(settings.MEDIA_ROOT, filepath)
    dirpath = os.path.dirname(filepath)

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    with open(filepath, 'wb') as fd:
        for chunk in data['file'].chunks():
            fd.write(chunk)

    readme_path = os.path.join(dirpath, "%s__README.txt" % timestr)
    with open(readme_path, 'w') as fd:
        fd.write(sub.comment)

    sub.file = filepath

    sub.save()
    messages.add_message(request, messages.SUCCESS, "Submission successful.")


def _create_event(team):
    event = TeamEvent(team=team)
    event.save()


def _check_yolo_avail(team):
    events = TeamEvent.objects.filter(team=team, used=False)
    if events:
        return events[0]
    return False


def _remove_attack(team):
    att = Attack.objects.filter(receiver=team, started=True, over=False)
    if len(att) == 1:
        att = att[0]
        att.over = True
        att.save()
    elif len(att) > 1:
        att_num = len(att)
        num_remove = att_num * 2 / 3
        att = att[0:num_remove - 1]
        for one_att in att:
            one_att.over = True
            one_att.save()
