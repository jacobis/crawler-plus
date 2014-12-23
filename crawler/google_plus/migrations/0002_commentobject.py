# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google_plus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('json', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
