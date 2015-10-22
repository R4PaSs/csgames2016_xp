# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_auto_20151014_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
