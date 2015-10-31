# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_auto_20151022_0459'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='original_creation',
            field=models.BooleanField(default=False, help_text='This card is fan-made and is not available in the game.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.ImageField(upload_to=web.models.card_upload_to),
            preserve_default=True,
        ),
    ]
