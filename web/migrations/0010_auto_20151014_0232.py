# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0009_auto_20150929_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='added_by',
            field=models.ForeignKey(related_name='added_cards', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='modified_by',
            field=models.ForeignKey(related_name='modified_cards', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='skill_value',
            field=models.PositiveIntegerField(help_text='The number you see in the sentence that explains what is the effect of the skill at this stage.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
