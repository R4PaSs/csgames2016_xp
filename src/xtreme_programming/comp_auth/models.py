from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    token = models.SlugField()
    user = models.OneToOneField(User, null=True)
    display_name = models.CharField(max_length=128)

    def __repr__(self):
        return str(self.name)
