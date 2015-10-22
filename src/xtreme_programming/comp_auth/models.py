from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    token = models.SlugField()


class Participant(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team)
