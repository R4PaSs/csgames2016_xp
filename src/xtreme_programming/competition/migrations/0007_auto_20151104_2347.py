# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0006_auto_20151104_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attack',
            name='attacker',
            field=models.ForeignKey(to='comp_auth.Team', related_name='attacks_out'),
        ),
        migrations.AlterField(
            model_name='attack',
            name='receiver',
            field=models.ForeignKey(to='comp_auth.Team', related_name='attacks_in'),
        ),
    ]
