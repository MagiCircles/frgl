# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_card_how_to_obtain'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='stars',
            field=models.PositiveIntegerField(null=True, verbose_name='Stars', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='how_to_obtain',
            field=models.TextField(help_text="For event or special songs cards. Leave empty if it's only obtainable in recruitment.", null=True, verbose_name='How to get it?', blank=True),
            preserve_default=True,
        ),
    ]
