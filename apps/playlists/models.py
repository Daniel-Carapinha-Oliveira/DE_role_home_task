from django.db import models


class Playlist(models.Model):
    id = models.AutoField(
        db_column='PlaylistId',
        primary_key=True
    )
    name = models.CharField(
        max_length=128,
        verbose_name='name',
        db_column='Name',
        unique=True
    )

    class Meta:
        db_table = 'Playlist'
        ordering = ['name']
        verbose_name = 'playlist'
        verbose_name_plural = 'playlists'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)


class PlaylistTrack(models.Model):
    pk = models.CompositePrimaryKey(
        'playlist', 'track'
    )

    playlist = models.ForeignKey(
        'playlists.Playlist',
        related_name='tracks',
        on_delete=models.CASCADE,
        verbose_name='playlist',
        db_column='PlaylistId',
    )
    track = models.ForeignKey(
        'music.Track',
        related_name='playlists',
        on_delete=models.PROTECT,
        verbose_name='track',
        db_column='TrackId',
    )

    class Meta:
        db_table = 'PlaylistTrack'

    def __str__(self):
        return f'{self.playlist} - {self.track}'

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)
