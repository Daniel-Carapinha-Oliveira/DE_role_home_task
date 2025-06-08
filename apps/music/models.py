from django.core.validators import MinValueValidator
from django.db import models


class Album(models.Model):
    id = models.AutoField(
        db_column='AlbumId',
        primary_key=True,
    )
    title = models.CharField(
        max_length=128,
        verbose_name='title',
        db_column='Title',
    )

    artist = models.ForeignKey(
        'music.Artist',
        on_delete=models.PROTECT,
        related_name='albums',
        verbose_name='artist',
        db_column='ArtistId'
    )

    class Meta:
        db_table = 'Album'
        ordering = ['title']
        verbose_name = 'album'
        verbose_name_plural = 'albums'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)


class Artist(models.Model):
    id = models.AutoField(
        db_column='ArtistId',
        primary_key=True
    )
    name = models.CharField(
        max_length=128,
        verbose_name='name',
        db_column='Name',
    )

    class Meta:
        db_table = 'Artist'
        ordering = ['name']
        verbose_name = 'artist'
        verbose_name_plural = 'artists'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)


class Genre(models.Model):
    id = models.AutoField(
        db_column='GenreId',
        primary_key=True
    )
    name = models.CharField(
        max_length=128,
        verbose_name='name',
        db_column='Name',
        unique=True
    )

    class Meta:
        db_table = 'Genre'
        ordering = ['name']
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)


class Track(models.Model):
    id = models.AutoField(
        db_column='TrackId',
        primary_key=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='name',
        db_column='Name',
    )
    composer = models.CharField(
        max_length=128,
        verbose_name='composer',
        db_column='Composer',
    )
    milliseconds = models.PositiveIntegerField(
        verbose_name='duration',
        db_column='Milliseconds'
    )
    bytes = models.PositiveIntegerField(
        verbose_name='size',
        db_column='Bytes',
    )
    unit_price = models.DecimalField(
        verbose_name='price',
        db_column='UnitPrice',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )

    album = models.ForeignKey(
        'music.Album',
        on_delete=models.PROTECT,
        related_name='tracks',
        db_column='AlbumId',
    )
    media_type = models.ForeignKey(
        'music.MediaType',
        on_delete=models.PROTECT,
        related_name='tracks',
        db_column='MediaTypeId'
    )
    genre = models.ForeignKey(
        'music.Genre',
        on_delete=models.PROTECT,
        related_name='tracks',
        db_column='GenreId',
    )

    class Meta:
        db_table = 'Track'
        ordering = ['name']
        verbose_name = 'track'
        verbose_name_plural = 'tracks'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)


class MediaType(models.Model):
    id = models.AutoField(
        db_column='MediaTypeId',
        primary_key=True
    )
    name = models.CharField(
        max_length=128,
        verbose_name='name',
        db_column='Name',
        unique=True
    )

    class Meta:
        db_table = 'MediaType'
        ordering = ['name']
        verbose_name = 'media type'
        verbose_name_plural = 'media types'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)
