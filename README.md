# Xtreme Programming Competition

## Deployment

``` bash
docker-compose build
docker-compose run xp bash

# You should now have a bash on the xp container
cd /opt/xp/src/xtreme_programming
python manage.py syncdb
python create_teams.py
python manage.py syncchallenges
python manage.py createsuperuser

# All setup... go back to your default shell
exit

docker-compose up
```

`http://localhost:8000/

From here the service should be accessible on localhost port 8000
