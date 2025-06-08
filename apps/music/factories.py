import factory

from apps.music.models import (
    Album,
    Artist,
    Genre,
    Track,
    MediaType
)


class AlbumFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f'title{n}')
    artist = factory.SubFactory('apps.music.factories.ArtistFactory')

    class Meta:
        model = Album


class ArtistFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')

    class Meta:
        model = Artist


class GenreFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')

    class Meta:
        model = Genre


class TrackFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')
    composer = factory.Sequence(lambda n: f'composer{n}')
    milliseconds = factory.Faker('random_int', min=1000, max=500000)
    bytes = factory.Faker('random_int', min=1000, max=10000000)
    unit_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    album = factory.SubFactory('apps.music.factories.AlbumFactory')
    media_type = factory.SubFactory('apps.music.factories.MediaTypeFactory')
    genre = factory.SubFactory('apps.music.factories.GenreFactory')

    class Meta:
        model = Track


class MediaTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')

    class Meta:
        model = MediaType
