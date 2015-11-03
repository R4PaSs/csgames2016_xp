import os, django
import string
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xtreme_programming.settings")
django.setup()

from django.contrib.auth.models import User

from comp_auth.models import Team

animals = ["alligator", "ant", "bear", "bee", "bird", "camel", "cat", "cheetah", 
           "chicken", "chimpanzee", "cow", "crocodile", "deer", "dog",
           "dolphin", "duck", "eagle", "elephant", "fish", "fly", "fox", "frog",
           "giraffe", "goat", "goldfish", "hamster", "hippopotamus", "horse", 
           "kangaroo", "kitten", "lion", "lobster", "monkey", "octopus", "owl",
           "panda", "pig", "puppy", "rabbit", "rat", "scorpion", "seal", 
           "shark", "sheep", "snail", "snake", "spider", "squirrel", "tiger", 
           "turtle", "wolf", "zebra"]

Team.objects.all().delete()
User.objects.all().delete()
for num in range(30):
    prefix = animals[random.randrange(len(animals) - 1)]
    suffix = animals[random.randrange(len(animals) - 1)] + "s"
    team_name = prefix + " " + suffix

    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(32))

    new_team = Team()
    new_user = User(username=team_name + "_user")
    new_user.save()

    print(team_name)
    print(token)
    new_team.name = team_name
    new_team.token = token
    new_team.user = new_user
    new_team.save()

