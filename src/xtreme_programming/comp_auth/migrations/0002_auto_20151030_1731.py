# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comp_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='team',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='user',
        ),
        migrations.AddField(
            model_name='team',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
    ]
