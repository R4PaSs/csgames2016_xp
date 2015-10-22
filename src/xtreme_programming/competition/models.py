from django.db import models

from comp_auth.models import Team


class Challenge(models.Model):
    length = models.IntegerField()
    title_EN = models.CharField(max_length=128)
    title_FR = models.CharField(max_length=128)
    description_EN = models.TextField()
    description_FR = models.TextField()
    end = models.DateTimeField(null=True, blank=True)


class Submission(models.Model):
    challenge = models.ForeignKey(Challenge)
    time = models.DateTimeField()
    file = models.FileField()
    comment = models.TextField()
    team = models.ForeignKey(Team)
