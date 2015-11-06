from django.contrib import admin

from .models import Challenge, Submission, TeamEvent, Attack

admin.site.register(Challenge)
admin.site.register(Submission)
admin.site.register(TeamEvent)
admin.site.register(Attack)
