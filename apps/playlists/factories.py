import factory

from apps.playlists.models import Playlist, PlaylistTrack


class PlaylistFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')

    class Meta:
        model = Playlist


class PlaylistTrackFactory(factory.django.DjangoModelFactory):
    playlist = factory.SubFactory('apps.playlists.factories.PlaylistFactory')
    track = factory.SubFactory('apps.music.factories.TrackFactory')

    class Meta:
        model = PlaylistTrack
