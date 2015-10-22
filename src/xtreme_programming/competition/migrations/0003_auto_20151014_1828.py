# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0002_challenge_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='end',
            field=models.DateTimeField(blank=True),
        ),
    ]
