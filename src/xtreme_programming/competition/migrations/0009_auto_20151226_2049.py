# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0008_auto_20151106_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='attack',
            name='attack_name',
            field=models.CharField(default='past', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attack',
            name='distributed',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attack',
            name='attacker',
            field=models.ForeignKey(related_name='attacker', to='comp_auth.Team'),
        ),
        migrations.AlterField(
            model_name='attack',
            name='receiver',
            field=models.ForeignKey(related_name='attacked', to='comp_auth.Team'),
        ),
    ]
