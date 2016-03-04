import os, django
import csv
import string
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xtreme_programming.settings")
django.setup()

from django.contrib.auth.models import User

from comp_auth.models import Team

Team.objects.all().delete()
User.objects.all().delete()

with open('teams.csv', 'r') as csvfile:
    teams = csv.DictReader(csvfile)
    for team_row in teams:
        display_name = team_row["Team Name"]
        team_name = team_row["Team Number"]
        token = team_row["Token"]

        new_team = Team()
        new_user = User(username=team_name + "_user")
        new_user.save()

        print(team_name)
        print(token)
        new_team.name = team_name
        new_team.token = token
        new_team.user = new_user
        new_team.save()

