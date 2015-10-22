# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('length', models.IntegerField()),
                ('title_EN', models.CharField(max_length=128)),
                ('title_FR', models.CharField(max_length=128)),
                ('description_EN', models.TextField()),
                ('description_FR', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('file', models.FileField(upload_to='')),
                ('comment', models.TextField()),
                ('challenge', models.ForeignKey(to='competition.Challenge')),
                ('team', models.ForeignKey(to='comp_auth.Team')),
            ],
        ),
    ]
