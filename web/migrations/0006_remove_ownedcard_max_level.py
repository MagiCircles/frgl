# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20150919_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ownedcard',
            name='max_level',
        ),
    ]
