# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=12, choices=[(b'reward', 'Reward'), (b'boost', 'Boost'), (b'unlock', 'Unlock'), (b'stageup', 'Stage Up')])),
                ('rarity', models.CharField(blank=True, max_length=12, null=True, choices=[(b'C', 'Common'), (b'R', 'Rare'), (b'SR', 'Super Rare'), (b'UR', 'Ultra Rare')])),
                ('image', models.ImageField(upload_to=b'cards')),
                ('attributes', models.CharField(max_length=100, null=True, blank=True)),
                ('stage_number', models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)])),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('sentence', models.CharField(max_length=200, null=True, blank=True)),
                ('add_value', models.PositiveIntegerField(null=True, blank=True)),
                ('reward_type', models.CharField(blank=True, max_length=20, null=True, choices=[(b'glee', 'Glee Coin'), (b'token', 'Story Token'), (b'card', 'Story Card'), (b'pass', 'Hall Pass'), (b'coupon', 'Premium Chance Coupon'), (b'eventtoken', 'Event Token'), (b'ticket', 'Tickets')])),
                ('max_level', models.PositiveIntegerField(null=True, blank=True)),
                ('minimum_performance', models.PositiveIntegerField(null=True, blank=True)),
                ('maximum_performance', models.PositiveIntegerField(null=True, blank=True)),
                ('max_level_reward', models.PositiveIntegerField(null=True, blank=True)),
                ('skill', models.CharField(blank=True, max_length=60, null=True, choices=[(b'overthebar', 'Over the bar'), (b'pitchperfect', 'Pitch Perfect'), (b'greattiming', 'Great Timing'), (b'vocalrun', 'Vocal Run'), (b'extraeffort', 'Extra Effort')])),
                ('skill_value', models.PositiveIntegerField(null=True, blank=True)),
                ('trigger_value', models.PositiveIntegerField(null=True, blank=True)),
                ('trigger_chance', models.PositiveIntegerField(null=True, blank=True)),
                ('parent', models.ForeignKey(related_name='children', to='web.Card', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('image', models.ImageField(upload_to=b'performers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='card',
            name='performer',
            field=models.ForeignKey(related_name='cards', to='web.Performer', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='card',
            unique_together=set([('parent', 'stage_number')]),
        ),
    ]
