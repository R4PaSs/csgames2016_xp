from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import index, problem, start, update, submit, attack, monitor, \
    update_monitor, tutorial, stop, wait, done, ready, reset

urlpatterns = [
    url(r'^$', tutorial, name="tutorial"),
    url(r'^start/$', start, name="start"),
    url(r'^stop/$', stop, name="stop"),
    url(r'^problem/(?P<cid>[0-9]+)$', problem, name="problem"),
    url(r'^update/$', update, name="update"),
    url(r'^attack/$', attack, name="attack"),
    url(r'^monitor/$', monitor, name="monitor"),
    url(r'^update_monitor/$', update_monitor, name="update_monitor"),
    url(r"^submit/(?P<cid>[0-9]+)$", submit, name="submit"),
    url(r'^play/$', index, name="index"),
    url(r'^wait/$', wait, name="wait"),
    url(r'^done/$', done, name="done"),
    url(r'^ready/$', ready, name="ready"),
    url(r'^reset/$', reset, name="reset"),
]
