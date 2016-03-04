# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp_auth', '0003_auto_20151226_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='display_name',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
