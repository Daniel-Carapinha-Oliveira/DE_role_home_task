# Generated by Django 5.2.2 on 2025-06-08 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(db_column='PlaylistId', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=128, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'playlist',
                'verbose_name_plural': 'playlists',
                'db_table': 'Playlist',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PlaylistTrack',
            fields=[
                ('pk', models.CompositePrimaryKey('playlist', 'track', blank=True, editable=False, primary_key=True, serialize=False)),
                ('playlist', models.ForeignKey(db_column='PlaylistId', on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='playlists.playlist', verbose_name='playlist')),
                ('track', models.ForeignKey(db_column='TrackId', on_delete=django.db.models.deletion.PROTECT, related_name='playlists', to='music.track', verbose_name='track')),
            ],
            options={
                'db_table': 'PlaylistTrack',
            },
        ),
    ]
