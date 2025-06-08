from pytest_factoryboy import register

from apps.music.factories import TrackFactory
from apps.playlists.factories import (
    PlaylistFactory,
    PlaylistTrackFactory
)

register(PlaylistFactory)
register(PlaylistTrackFactory)
register(TrackFactory)
