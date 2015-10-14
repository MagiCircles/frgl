# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20151014_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='how_to_obtain',
            field=models.TextField(null=True, verbose_name='How to get it?', blank=True),
            preserve_default=True,
        ),
    ]
