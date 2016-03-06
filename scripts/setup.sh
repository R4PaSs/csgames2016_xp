#!/bin/bash

echo "Preparing to setup databases..."
sleep 20

echo $PWD
if [[ $PWD/ = */scripts/ ]];
then
	cd ..
fi

echo $PWD
if [[ $PWD = / ]];
then
	cd /opt/xp/
fi

cd src/xtreme_programming
yes no | python manage.py syncdb
python create_teams.py
python manage.py syncchallenges

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'ppeposp@gmail.com', 'store170')" | python manage.py shell


chmod -R 777 /xp_media
chown -R www-data: /xp_media

