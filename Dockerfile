from python:2.7

# RUN apt-get -q update
# RUN apt-get -qy install -q vim python python-pip

RUN mkdir -p /opt/xp
ADD . /opt/xp

RUN pip install -r /opt/xp/requirements.txt

RUN cd /opt/xp/src/xtreme_programming && \
	python manage.py syncchallenges

CMD	\
	cd /opt/xp/src/xtreme_programming/ && \
	python manage.py runserver 0.0.0.0:8000
