# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20200730_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='alias',
            field=models.CharField(default=' ', unique=True, max_length=128),
            preserve_default=False,
        ),
    ]
