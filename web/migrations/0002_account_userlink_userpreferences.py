# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=20, verbose_name='Nickname', blank=True)),
                ('os', models.CharField(default=b'iOs', max_length=10, verbose_name='Operating System', choices=[(b'Android', b'Android'), (b'iOs', b'iOs')])),
                ('device', models.CharField(help_text='The modele of your device. Example: Nexus 5, iPhone 4, iPad 2, ...', max_length=150, null=True, verbose_name='Device', blank=True)),
                ('play_with', models.CharField(blank=True, max_length=30, null=True, verbose_name='Play with', choices=[(b'Thumbs', 'Thumbs'), (b'Fingers', 'All fingers'), (b'Index', 'Index fingers'), (b'Hand', 'One hand'), (b'Other', 'Other')])),
                ('accept_friend_requests', models.NullBooleanField(verbose_name='Accept friend requests on Facebook')),
                ('rank', models.PositiveIntegerField(null=True, verbose_name='Rank', blank=True)),
                ('account_id', models.PositiveIntegerField(help_text='To find your ID, tap the settings icon, then tap "Profile". Your ID is the number you see on top of the window.', null=True, verbose_name='ID', blank=True)),
                ('owner', models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20, verbose_name='Platform', choices=[(b'facebook', b'Facebook'), (b'twitter', b'Twitter'), (b'reddit', b'Reddit'), (b'schoolidolu', b'School Idol Tomodachi'), (b'line', b'LINE Messenger'), (b'tumblr', b'Tumblr'), (b'twitch', b'Twitch'), (b'steam', b'Steam'), (b'instagram', b'Instagram'), (b'youtube', b'YouTube'), (b'github', b'GitHub')])),
                ('value', models.CharField(help_text='Write your username only, no URL.', max_length=64, verbose_name='Username/ID', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\. ]*$', b'Only alphanumeric and - _ characters are allowed.')])),
                ('relevance', models.PositiveIntegerField(null=True, verbose_name='How often do you tweet/stream/post about Glee?', choices=[(0, 'Never'), (1, 'Sometimes'), (2, 'Often'), (3, 'Every single day')])),
                ('owner', models.ForeignKey(related_name='links', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(help_text='Write whatever you want. You can add formatting and links using Markdown.', null=True, verbose_name='Description', blank=True)),
                ('location', models.CharField(help_text='The city you live in. It might take up to 24 hours to update your location on the map.', max_length=200, null=True, verbose_name='Location', blank=True)),
                ('location_changed', models.BooleanField(default=False)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('status', models.CharField(max_length=12, null=True, choices=[(b'THANKS', b'Thanks'), (b'SUPPORTER', 'Idol Supporter'), (b'LOVER', 'Idol Lover'), (b'AMBASSADOR', 'Idol Ambassador'), (b'PRODUCER', 'Idol Producer'), (b'DEVOTEE', 'Ultimate Idol Devotee')])),
                ('donation_link', models.CharField(max_length=200, null=True, blank=True)),
                ('donation_link_title', models.CharField(max_length=100, null=True, blank=True)),
                ('favorite_performer', models.ForeignKey(related_name='fans', on_delete=django.db.models.deletion.SET_NULL, to='web.Performer', null=True)),
                ('following', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
