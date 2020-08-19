# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_blog_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='Like',
        ),
        migrations.AddField(
            model_name='blog',
            name='likedBy',
            field=models.ManyToManyField(related_name=b'likes', to='blogs.UserProfile'),
            preserve_default=True,
        ),
    ]
