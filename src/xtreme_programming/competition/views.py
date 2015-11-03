import datetime
import os
import time

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, render_to_response

from .models import Challenge, Submission
from .forms import SubmissionForm


NEXT_EXPIRE = None


@login_required()
def index(request):
    chals = Challenge.objects.all()

    for chal in chals:
        if chal.end:
            chal.end = int(time.mktime(chal.end.timetuple())) * 1000

    return render(request, 'competition/index.html',
                  context={'chals': chals})


# @user_passes_test(lambda u: u.is_superuser)
def start(request):
    initial_chals = Challenge.objects.order_by('?')\
            [0:settings.OPEN_CHALLENGE_COUNT]

    chals = Challenge.objects.all()
    for chal in chals:
        chal.end = None
        chal.save()

    for chal in initial_chals:
        _start_challenge(chal)

    return render_to_response('competition/index.html')


def update(request):
    _check_open_challenges()
    return JsonResponse(_filter_chals())


def problem(request, cid):
    context = {}

    if _is_open(cid):
        chal = Challenge.objects.get(pk=cid)
        context['chal'] = chal
        context['form'] = SubmissionForm(cid=cid)

    return render(request, 'competition/problem.html',
                  context=context)


def submit(request, cid):
    if _is_open(cid):
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            if _valid_zip(form.cleaned_data['file']):
                _save_submission(request, cid, form.cleaned_data)

                return JsonResponse({"id": cid}, status=200)

    return JsonResponse({"id": cid}, status=400)


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
