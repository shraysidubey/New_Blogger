# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_auto_20200816_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=500)),
                ('blog', models.ForeignKey(to='blogs.blog')),
                ('user', models.ForeignKey(to='blogs.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
