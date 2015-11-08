# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0007_auto_20151104_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamevent',
            name='team',
            field=models.ForeignKey(to='comp_auth.Team'),
        ),
    ]
