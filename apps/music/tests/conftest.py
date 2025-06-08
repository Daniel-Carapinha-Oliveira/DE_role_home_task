from pytest_factoryboy import register

from apps.music.factories import (
    AlbumFactory,
    ArtistFactory,
    GenreFactory,
    TrackFactory,
    MediaTypeFactory
)

register(AlbumFactory)
register(ArtistFactory)
register(GenreFactory)
register(TrackFactory)
register(MediaTypeFactory)
