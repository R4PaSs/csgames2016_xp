from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import index, problem, start, update

urlpatterns = [
    url(r'^start/$', start, name="start"),
    url(r'^problem/(?P<id>[0-9]+)$', problem, name="problem"),
    url(r'^update/$', update, name="update"),
    url(r'^$', index, name="index"),
]
