# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0009_auto_20151226_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('singleton_enforce', models.IntegerField(default=1, unique=True)),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
