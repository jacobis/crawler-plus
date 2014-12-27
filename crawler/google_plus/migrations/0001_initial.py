# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('published', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('activity_id', models.CharField(unique=True, max_length=100)),
                ('url', models.URLField()),
                ('verb', models.CharField(max_length=30)),
                ('annotation', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityJson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(unique=True, max_length=100)),
                ('json', models.TextField()),
                ('is_crawled', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_type', models.CharField(max_length=30)),
                ('object_id', models.CharField(max_length=100, blank=True)),
                ('content', models.TextField()),
                ('url', models.URLField()),
                ('plusoners', models.IntegerField()),
                ('resharers', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actor_id', models.CharField(unique=True, max_length=100)),
                ('display_name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('image', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_type', models.CharField(max_length=30)),
                ('display_name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('url', models.URLField()),
                ('image', models.URLField(blank=True)),
                ('full_image', models.URLField(blank=True)),
                ('embed', models.URLField(blank=True)),
                ('activity_object', models.ForeignKey(to='google_plus.ActivityObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=50)),
                ('verb', models.CharField(max_length=30)),
                ('comment_id', models.CharField(unique=True, max_length=100)),
                ('published', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('content', models.TextField()),
                ('self_link', models.URLField()),
                ('plusoners', models.IntegerField()),
                ('activity_object', models.ForeignKey(to='google_plus.ActivityObject')),
                ('actor', models.ForeignKey(to='google_plus.Actor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentJson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_id', models.CharField(max_length=100)),
                ('object_id', models.CharField(max_length=100)),
                ('json', models.TextField()),
                ('is_crawled', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_object',
            field=models.ForeignKey(to='google_plus.ActivityObject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='actor',
            field=models.ForeignKey(to='google_plus.Actor'),
            preserve_default=True,
        ),
    ]
