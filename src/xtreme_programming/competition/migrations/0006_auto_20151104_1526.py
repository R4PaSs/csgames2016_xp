# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp_auth', '0002_auto_20151030_1731'),
        ('competition', '0005_teamevents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attack',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('attack_number', models.IntegerField()),
                ('started', models.BooleanField(default=False)),
                ('over', models.BooleanField(default=False)),
                ('attacker', models.OneToOneField(to='comp_auth.Team', related_name='attacks_out')),
                ('receiver', models.OneToOneField(to='comp_auth.Team', related_name='attacks_in')),
            ],
        ),
        migrations.CreateModel(
            name='TeamEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('used', models.BooleanField(default=False)),
                ('team', models.OneToOneField(to='comp_auth.Team')),
            ],
        ),
        migrations.RemoveField(
            model_name='teamevents',
            name='team',
        ),
        migrations.DeleteModel(
            name='TeamEvents',
        ),
    ]
