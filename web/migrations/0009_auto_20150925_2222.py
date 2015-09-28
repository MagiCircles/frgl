# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20150925_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='accept_friend_requests',
            field=models.NullBooleanField(verbose_name='Accept friend requests on Facebook'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='os',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Operating System', choices=[(b'Android', b'Android'), (b'iOs', b'iOs')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userlink',
            name='relevance',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='How often do you tweet/stream/post about Glee?', choices=[(0, 'Never'), (1, 'Sometimes'), (2, 'Often'), (3, 'Every single day')]),
            preserve_default=True,
        ),
    ]
