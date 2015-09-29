# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20150928_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='max_level',
        ),
        migrations.RemoveField(
            model_name='card',
            name='max_level_reward',
        ),
        migrations.RemoveField(
            model_name='card',
            name='minimum_performance',
        ),
        migrations.AlterField(
            model_name='card',
            name='attributes',
            field=models.CharField(help_text='Also known as "song types".', max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='maximum_performance',
            field=models.PositiveIntegerField(help_text='Only provide this information for SRs and URs.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(help_text='Cheerio, Glam Girl, Believer, ...', max_length=200, null=True, verbose_name='Collection', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='rarity',
            field=models.CharField(default=b'C', max_length=12, choices=[(b'C', 'Common'), (b'R', 'Rare'), (b'SR', 'Super Rare'), (b'UR', 'Ultra Rare')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='sentence',
            field=models.CharField(help_text='The sentence you see when you get the story card.', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='skill',
            field=models.CharField(blank=True, max_length=60, null=True, help_text='Leave blank for common cards', choices=[(b'overthebar', 'Over the bar'), (b'pitchperfect', 'Pitch Perfect'), (b'greattiming', 'Great Timing'), (b'vocalrun', 'Vocal Run'), (b'extraeffort', 'Extra Effort')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='skill_value',
            field=models.PositiveIntegerField(help_text='The number you see in the sentence that explains what is the effect of the skill.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='trigger_chance',
            field=models.PositiveIntegerField(help_text='The % chance of skill activation.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='trigger_value',
            field=models.PositiveIntegerField(help_text='The number you see in the sentence that explains when the skill can be activated.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
