# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(to='blogs.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(unique=True, max_length=128),
        ),
    ]
