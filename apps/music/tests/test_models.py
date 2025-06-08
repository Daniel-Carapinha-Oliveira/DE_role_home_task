import pytest

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from apps.music.models import (
    Album,
    Artist,
    Genre,
    Track,
    MediaType
)

pytestmark = pytest.mark.django_db


class TestAlbumModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_title_max_length(self, album_factory):
        title = 'x' * 256
        with pytest.raises(ValidationError):
            album_factory(title=title)

    def test_fk_artist_on_delete_protect(self, album_factory, artist_factory):
        obj = artist_factory()
        album_factory(artist=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_str_method(self, album_factory):
        obj = album_factory()
        assert obj.__str__() == obj.title

    def test_ordering(self, album_factory):
        albums = album_factory.create_batch(5)
        expected_order = sorted(albums, key=lambda k: k.title)
        assert list(Album.objects.all()) == expected_order

    def test_save_calls_full_clean(self, album_factory, monkeypatch):
        album = album_factory()
        monkeypatch.setattr(album, 'full_clean', self.fake_full_clean)
        album.save()
        assert self.full_clean_calls == 1


class TestArtistModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_name_max_length(self, artist_factory):
        name = 'x' * 129
        with pytest.raises(ValidationError):
            artist_factory(name=name)

    def test_str_method(self, artist_factory):
        obj = artist_factory()
        assert obj.__str__() == obj.name

    def test_ordering(self, artist_factory):
        albums = artist_factory.create_batch(5)
        expected_order = sorted(albums, key=lambda k: k.name)
        assert list(Artist.objects.all()) == expected_order

    def test_save_calls_full_clean(self, artist_factory, monkeypatch):
        artist = artist_factory()
        monkeypatch.setattr(artist, 'full_clean', self.fake_full_clean)
        artist.save()
        assert self.full_clean_calls == 1


class TestGenreModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_name_max_length(self, genre_factory):
        name = 'x' * 129
        with pytest.raises(ValidationError):
            genre_factory(name=name)

    def test_str_method(self, genre_factory):
        obj = genre_factory()
        assert obj.__str__() == obj.name

    def test_ordering(self, genre_factory):
        genres = genre_factory.create_batch(5)
        expected_order = sorted(genres, key=lambda k: k.name)
        assert list(Genre.objects.all()) == expected_order

    def test_save_calls_full_clean(self, genre_factory, monkeypatch):
        genre = genre_factory()
        monkeypatch.setattr(genre, 'full_clean', self.fake_full_clean)
        genre.save()
        assert self.full_clean_calls == 1


class TestTrackModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_name_max_length(self, track_factory):
        name = 'x' * 256
        with pytest.raises(ValidationError):
            track_factory(name=name)

    def test_composer_max_length(self, track_factory):
        composer = 'x' * 129
        with pytest.raises(ValidationError):
            track_factory(composer=composer)

    def test_milliseconds_positive_number(self, track_factory):
        with pytest.raises(ValidationError):
            track_factory(milliseconds=-1)

    def test_milliseconds_integer_number(self, track_factory):
        track = track_factory.build(milliseconds=1.2)
        with pytest.raises(ValidationError):
            track.full_clean()

    def test_bytes_positive_number(self, track_factory):
        with pytest.raises(ValidationError):
            track_factory(bytes=-1)

    def test_bytes_integer_number(self, track_factory):
        track = track_factory.build(bytes=1.2)
        with pytest.raises(ValidationError):
            track.full_clean()

    def test_unit_price_accepts_only_zero_and_positive(self, track_factory):
        with pytest.raises(ValidationError):
            track_factory(unit_price=-1.2)

    def test_fk_album_on_delete_protect(self, track_factory, album_factory):
        obj = album_factory()
        track_factory(album=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_fk_media_type_on_delete_protect(self, track_factory, media_type_factory):
        obj = media_type_factory()
        track_factory(media_type=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_fk_genre_on_delete_protect(self, track_factory, genre_factory):
        obj = genre_factory()
        track_factory(genre=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_str_method(self, track_factory):
        obj = track_factory(name='Example')
        assert obj.__str__() == obj.name

    def test_ordering(self, track_factory):
        tracks = track_factory.create_batch(5)
        expected_order = sorted(tracks, key=lambda k: k.name)
        assert list(Track.objects.all()) == expected_order

    def test_save_calls_full_clean(self, track_factory, monkeypatch):
        track = track_factory()
        monkeypatch.setattr(track, 'full_clean', self.fake_full_clean)
        track.save()
        assert self.full_clean_calls == 1


class TestMediaTypeModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_name_max_length(self, media_type_factory):
        name = 'x' * 129
        with pytest.raises(ValidationError):
            media_type_factory(name=name)

    def test_str_method(self, media_type_factory):
        obj = media_type_factory()
        assert obj.__str__() == obj.name

    def test_ordering(self, media_type_factory):
        genres = media_type_factory.create_batch(5)
        expected_order = sorted(genres, key=lambda k: k.name)
        assert list(MediaType.objects.all()) == expected_order

    def test_save_calls_full_clean(self, media_type_factory, monkeypatch):
        media_type = media_type_factory()
        monkeypatch.setattr(media_type, 'full_clean', self.fake_full_clean)
        media_type.save()
        assert self.full_clean_calls == 1
