from python:2.7

RUN apt-get -q update
RUN apt-get -qy install -q vim apache2 libapache2-mod-wsgi

RUN mkdir -p /opt/xp
ADD . /opt/xp

RUN pip install -r /opt/xp/requirements.txt

# Configure apache and mod_wsgi
RUN cat /opt/xp/apache2_add.conf >> /etc/apache2/apache2.conf

RUN update-rc.d -f  apache2 remove
RUN chown -R www-data:www-data /opt/xp/src/xtreme_programming

RUN mkdir -p /var/www/xp/static
RUN mkdir -p /xp_media

RUN chown -R www-data: /var/www/xp/
RUN chown -R www-data: /xp_media

RUN chmod 700 -R /xp_media

CMD \
	service apache2 stop && \
	cd /opt/xp/src/xtreme_programming/ && \
	python manage.py collectstatic --noinput && \
	/usr/sbin/apache2ctl -DFOREGROUND
