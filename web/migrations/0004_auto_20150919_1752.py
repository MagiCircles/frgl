# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20150919_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnedCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('max_level', models.BooleanField(default=False, verbose_name='Max Leveled')),
                ('account', models.ForeignKey(related_name='ownedcards', verbose_name='Account', to='web.Account')),
                ('card', models.ForeignKey(related_name='ownedcards', to='web.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='private',
            field=models.BooleanField(default=False, help_text='If your profile is private, only you can see your cards, event participations and cleared songs.', verbose_name='Private Profile'),
            preserve_default=True,
        ),
    ]
