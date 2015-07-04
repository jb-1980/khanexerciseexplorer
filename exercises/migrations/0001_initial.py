# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommonCore',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('category', models.CharField(max_length=128)),
                ('strand', models.CharField(max_length=128)),
                ('standard', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommonCoreMap',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ka_id', models.CharField(unique=True, max_length=128)),
                ('name', models.CharField(unique=True, max_length=512)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
                ('image_url_256', models.URLField(max_length=512)),
                ('ka_url', models.URLField(max_length=512)),
                ('views', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MissionMap',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('exercise', models.ForeignKey(to='exercises.Exercises', to_field='ka_id')),
            ],
        ),
        migrations.CreateModel(
            name='Missions',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('sequenceid', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisites',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('requiredfor', models.CharField(max_length=512)),
                ('exercise', models.ForeignKey(to='exercises.Exercises', to_field='name')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedVideos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('exercise', models.ForeignKey(to='exercises.Exercises', to_field='name')),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
                ('sequenceid', models.FloatField(default=0.0)),
                ('mission', models.ForeignKey(to='exercises.Missions', to_field='name')),
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('videoid', models.CharField(unique=True, max_length=512)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
                ('ka_url', models.URLField(max_length=512)),
            ],
        ),
        migrations.AddField(
            model_name='relatedvideos',
            name='videoid',
            field=models.ForeignKey(to='exercises.Videos', to_field='videoid'),
        ),
        migrations.AddField(
            model_name='missionmap',
            name='unit',
            field=models.ForeignKey(to='exercises.Units'),
        ),
        migrations.AddField(
            model_name='commoncoremap',
            name='exercise',
            field=models.ForeignKey(to='exercises.Exercises', to_field='name'),
        ),
        migrations.AddField(
            model_name='commoncoremap',
            name='standard',
            field=models.ForeignKey(to='exercises.CommonCore', to_field='standard'),
        ),
        migrations.AlterUniqueTogether(
            name='units',
            unique_together=set([('name', 'mission')]),
        ),
    ]
