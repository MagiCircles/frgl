# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_account_userlink_userpreferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='facebook',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='twitter',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
    ]
