from python:2.7

RUN apt-get -q update
RUN apt-get -qy install -q vim apache2 libapache2-mod-wsgi

RUN mkdir -p /opt/xp
ADD . /opt/xp

RUN pip install -r /opt/xp/requirements.txt

# Configure apache and mod_wsgi
RUN echo "" >> /etc/apache2/apache2.conf
RUN echo "Alias /static/ /var/www/xp/static/" >> /etc/apache2/apache2.conf
RUN echo "Alias /fonts/ /var/www/xp/static/fonts/" >> /etc/apache2/apache2.conf
RUN echo "" >> /etc/apache2/apache2.conf
RUN echo "<Directory /var/www/xp/static>" >> /etc/apache2/apache2.conf
RUN echo "Require all granted" >> /etc/apache2/apache2.conf
RUN echo "</Directory>" >> /etc/apache2/apache2.conf
RUN echo "" >> /etc/apache2/apache2.conf
RUN echo "WSGIScriptAlias / /opt/xp/src/xtreme_programming/xtreme_programming/wsgi.py" >> /etc/apache2/apache2.conf
RUN echo "WSGIPythonPath /opt/xp/src/xtreme_programming" >> /etc/apache2/apache2.conf
RUN echo "" >> /etc/apache2/apache2.conf
RUN echo "<Directory /opt/xp/src/xtreme_programming/xtreme_programming>" >> /etc/apache2/apache2.conf
RUN echo "<Files wsgi.py>" >> /etc/apache2/apache2.conf
RUN echo "Require all granted" >> /etc/apache2/apache2.conf
RUN echo "</Files>" >> /etc/apache2/apache2.conf
RUN echo "</Directory>" >> /etc/apache2/apache2.conf
RUN echo "" >> /etc/apache2/apache2.conf

RUN update-rc.d -f  apache2 remove
RUN chown -R www-data:www-data /opt/xp/src/xtreme_programming

RUN mkdir -p /var/www/xp/static
RUN chown -R www-data: /var/www/xp/

CMD \
	service apache2 stop && \
	cd /opt/xp/src/xtreme_programming/ && \
	python manage.py collectstatic --noinput && \
	sleep 5 && \
	/usr/sbin/apache2ctl -D FOREGROUND
