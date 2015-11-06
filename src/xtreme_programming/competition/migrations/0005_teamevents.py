# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp_auth', '0002_auto_20151030_1731'),
        ('competition', '0004_auto_20151014_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamEvents',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('used', models.BooleanField(default=False)),
                ('team', models.OneToOneField(to='comp_auth.Team')),
            ],
        ),
    ]
