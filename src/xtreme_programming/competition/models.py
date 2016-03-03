from django.db import models

from comp_auth.models import Team

from .singleton import SingletonModel


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


class TeamEvent(models.Model):
    team = models.ForeignKey(Team)
    used = models.BooleanField(default=False)


class Attack(models.Model):
    attacker = models.ForeignKey(Team, related_name='attacker')
    receiver = models.ForeignKey(Team, related_name='attacked')
    attack_number = models.IntegerField()
    attack_name = models.CharField(max_length=64)
    distributed = models.BooleanField()
    started = models.BooleanField(default=False)
    over = models.BooleanField(default=False)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.distributed:
            return "Distributed %s from %s" % (self.attack_name, self.attacker.name)
        else:
            return "%s from %s to %s" % (self.attack_name, self.attacker.name,
                                         self.receiver.name)


class GlobalStatus(SingletonModel):
    status = models.CharField(max_length=32)
