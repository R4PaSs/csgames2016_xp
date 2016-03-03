#!/bin/bash

python manage.py syncdb
python create_teams.py
python manage.py syncchallenges
python manage.py createsuperuser
