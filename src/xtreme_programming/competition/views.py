import datetime
import json
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
    completed = Challenge.objects.filter(submission__team=request.user.team)
    failed = []

    for chal in chals:
        if chal.end:
            if chal.end < datetime.datetime.now():
                failed.append(chal)
            chal.end = int(time.mktime(chal.end.timetuple())) * 1000

    return render(request, 'competition/index.html',
                  context={'chals': chals,
                           'completed': completed,
                           'failed': failed})


@user_passes_test(lambda u: u.is_superuser)
def start(request):

    _init_cleanup()

    initial_chals = Challenge.objects.order_by('id')
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
    data['chals'] = _filter_chals(request.user.team)
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
                             attack_number=rand_idx,
                             distributed=True,
                             attack_name=attack_meta["name"])
                atk.save()
        elif attack_meta["type"] == "targeted":
            recv = randrange(0, 2)
            if recv == 0:
                recv = team
            else:
                recv = Team.objects.all().order_by('?')[0]

            atk = Attack(attacker=team,
                         receiver=recv,
                         attack_number=rand_idx,
                         distributed=False,
                         attack_name=attack_meta["name"])
            atk.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)


@user_passes_test(lambda u: u.is_superuser)
def monitor(request):
    teams = Team.objects.all().order_by('name')
    team_info = []

    color_palette = ["#67DB96",
                     "#D14DE0",
                     "#DF4A2A",
                     "#6C9BD1",
                     "#D0D73A",
                     "#82724C",
                     "#DB3878",
                     "#DFA035",
                     "#7AE42C",
                     "#CB88DA",
                     "#52A335",
                     "#54927D",
                     "#D5C97B",
                     "#C0D5DC",
                     "#66DFCE",
                     "#A67076",
                     "#8A69E3",
                     "#D8AED0",
                     "#D5926D",
                     "#93872F",
                     "#C1E2B0",
                     "#4B7631",
                     "#677A87",
                     "#C36595",
                     "#D744B0",
                     "#5F7FDB",
                     "#C9B6A0",
                     "#D0555D",
                     "#B76130",
                     "#766B9F",
                     "#B3D866",
                     "#63B9D0",
                     "#6BE261",
                     "#9654AF",
                     "#71A164"]

    for idx, team in enumerate(teams):
        info = {
            'id': team.id,
            'name': team.name,
            'color': color_palette[idx % len(color_palette)]
        }
        team_info.append(info)

    return render(request, 'competition/monitor.html',
                  context={'team_info': json.dumps(team_info)})


@user_passes_test(lambda u: u.is_superuser)
def update_monitor(request):

    data = {'attacks': []}
    attacks = Attack.objects.filter(over=False, started=True).order_by('id')

    for attack in attacks:

        att_dict = {
            'attacker': attack.attacker_id,
            'attacker_name': attack.attacker.name,
            'receiver': attack.receiver_id,
            'receiver_name': attack.receiver.name,
            'name': attack.attack_name,
            'distributed': attack.distributed
        }

        data['attacks'].append(att_dict)

    return JsonResponse(data)


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


def _filter_chals(team):
    chals = Challenge.objects.all()
    submitted = Challenge.objects.filter(submission__team=team)
    filtered = {}
    for chal in chals:
        js_end = None

        if chal.end:
            js_end = int(time.mktime(chal.end.timetuple())) * 1000

        fchal = {
            "id": chal.id,
            "end": js_end,
            "submitted": False
        }

        if chal in submitted:
            fchal["submitted"] = True

        filtered[chal.id] = fchal

    return filtered


def _check_open_challenges():
    open_chals = Challenge.objects.filter(end__gt=datetime.datetime.now())\
        .count()
    if open_chals < settings.OPEN_CHALLENGE_COUNT:
        try:
            new_chal = Challenge.objects.filter(end__isnull=True)\
                .order_by('id')[0]
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
    # messages.add_message(request, messages.SUCCESS, "Submission successful.")


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
