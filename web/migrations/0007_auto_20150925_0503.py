# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0006_remove_ownedcard_max_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=300, choices=[(b'Added a card', 'Added a card'), (b'Rank Up', 'Rank Up'), (b'Ranked in event', 'Ranked in event'), (b'Followed', 'Followed')])),
                ('rank', models.PositiveIntegerField(null=True, blank=True)),
                ('account', models.ForeignKey(related_name='activities', blank=True, to='web.Account', null=True)),
                ('likes', models.ManyToManyField(related_name='liked_activities', to=settings.AUTH_USER_MODEL)),
                ('ownedcard', models.ForeignKey(blank=True, to='web.OwnedCard', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([('account', 'message', 'rank'), ('account', 'message', 'ownedcard')]),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='status',
            field=models.CharField(max_length=12, null=True, choices=[(b'THANKS', b'Thanks'), (b'SUPPORTER', 'Gleek'), (b'LOVER', 'Super Gleek'), (b'AMBASSADOR', 'Extreme Gleek'), (b'PRODUCER', 'Gleek Master'), (b'DEVOTEE', 'Ultimate Glee Lover')]),
            preserve_default=True,
        ),
    ]
