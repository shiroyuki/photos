from photos.prototype import ICommand

class MetadataAggregator(ICommand):
    """ Inspect the photo metadata. """

    def __init__(self, archive):
        self.archive = archive

    def define(self, parser):
        parser.add_argument(
            '--debug',
            help='Enable the debugging mode.'
        )

    def execute(self, args):
        photo = self.archive.open(args.path)

        print('Location:  {}'.format(photo.location))
        print('SHA1 Hash: {}'.format(photo.hashsum))

        info = photo.info()

        for l in info:
            v = info[l]
            print('{:<20}: {}'.format(l, v))

class Inspector(ICommand):
    """ Inspect the photo metadata. """

    def __init__(self, archive):
        self.archive = archive

    def define(self, parser):
        parser.add_argument('path', help='The path to the image file.')

    def execute(self, args):
        photo = self.archive.open(args.path)

        print('Location:  {}'.format(photo.location))
        print('SHA1 Hash: {}'.format(photo.hashsum))

        info = photo.info()

        for l in info:
            v = info[l]
            print('{:<20}: {}'.format(l, v))