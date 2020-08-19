# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_blog_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='Like',
            field=models.ManyToManyField(related_name=b'Like', to='blogs.UserProfile'),
            preserve_default=True,
        ),
    ]
