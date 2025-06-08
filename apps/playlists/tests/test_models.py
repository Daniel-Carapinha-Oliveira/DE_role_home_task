import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from apps.playlists.models import Playlist, PlaylistTrack

pytestmark = pytest.mark.django_db


class TestPlaylistModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_name_max_length(self, playlist_factory):
        name = 'x' * 129
        with pytest.raises(ValidationError):
            playlist_factory(name=name)

    def test_name_unique_field(self, playlist_factory):
        obj = playlist_factory()
        with pytest.raises(ValidationError):
            playlist_factory(name=obj.name)

    def test_str_method(self, playlist_factory):
        obj = playlist_factory()
        assert obj.__str__() == obj.name

    def test_ordering(self, playlist_factory):
        playlists = playlist_factory.create_batch(5)
        expected_order = sorted(playlists, key=lambda k: k.name)
        assert list(Playlist.objects.all()) == expected_order

    def test_save_calls_full_clean(self, playlist_factory, monkeypatch):
        playlist = playlist_factory()
        monkeypatch.setattr(playlist, 'full_clean', self.fake_full_clean)
        playlist.save()
        assert self.full_clean_calls == 1


class TestPlaylistTrackModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_fk_playlist_on_delete_cascade(self, playlist_track_factory, playlist_factory):
        playlist = playlist_factory()

        playlist_track_factory(playlist=playlist)

        playlist.delete()

        assert not PlaylistTrack.objects.filter(playlist=playlist.pk).first()

    def test_fk_track_on_delete_protect(self, playlist_track_factory, track_factory):
        obj = track_factory()
        playlist_track_factory(track=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_str_method(self, playlist_track_factory):
        obj = playlist_track_factory()
        assert obj.__str__() == f'{obj.playlist} - {obj.track}'

    def test_save_calls_full_clean(self, playlist_track_factory, monkeypatch):
        playlist_track = playlist_track_factory()
        monkeypatch.setattr(playlist_track, 'full_clean', self.fake_full_clean)
        playlist_track.save()
        assert self.full_clean_calls == 1
