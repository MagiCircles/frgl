# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20150929_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='maximum_performance',
        ),
        migrations.AddField(
            model_name='card',
            name='maximum_performance_ability',
            field=models.PositiveIntegerField(help_text='The highest performance ability for this card at this stage.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='attributes',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='skill',
            field=models.CharField(blank=True, max_length=60, null=True, choices=[(b'overthebar', 'Over the bar'), (b'pitchperfect', 'Pitch Perfect'), (b'greattiming', 'Great Timing'), (b'vocalrun', 'Vocal Run'), (b'extraeffort', 'Extra Effort')]),
            preserve_default=True,
        ),
    ]
