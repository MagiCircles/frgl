# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20150925_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='os',
            field=models.CharField(default=b'iOs', max_length=10, null=True, verbose_name='Operating System', choices=[(b'Android', b'Android'), (b'iOs', b'iOs')]),
            preserve_default=True,
        ),
    ]
