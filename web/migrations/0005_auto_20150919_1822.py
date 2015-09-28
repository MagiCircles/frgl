# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20150919_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='accept_friend_requests',
            field=models.BooleanField(default=True, verbose_name='Accept friend requests on Facebook'),
            preserve_default=True,
        ),
    ]
