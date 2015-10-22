# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20151015_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='reward_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'glee', 'Glee Coin'), (b'token', 'Story Token'), (b'card', 'Story Card'), (b'pass', 'Hall Pass'), (b'coupon', 'Premium Chance Coupon'), (b'eventtoken', 'Event Token'), (b'ticket', 'Tickets'), (b'profile', 'Profile Icon')]),
            preserve_default=True,
        ),
    ]
