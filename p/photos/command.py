from photos.prototype import ICommand

class MetadataAggregator(ICommand):
    """ Inspect the photo metadata. """

    def __init__(self, service):
        self.service = service

    def define(self, parser):
        parser.add_argument(
            '--debug',
            help='Enable the debugging mode.'
        )
        parser.add_argument(
            'path',
            required=True,
            help='Enable the debugging mode.'
        )

    def execute(self, args):
        import os
        import re

        path_list = os.walk(args.path)

        re_expected_extensions = re.compile('.+\.(jpe?g|tiff|png)$', re.IGNORECASE)

        target_paths = []

        for inspected_path, _, file_paths in path_list:
            target_paths.extend([
                os.path.join(inspected_path, file_path)
                for file_path in file_paths
                if re_expected_extensions.search(file_path)
            ])

        total_count = len(target_paths)
        index = 0

        for target_path in target_paths:
            index += 1

            print('({}/{}) Analyzing {}...'.format(index, total_count, target_path))

            self.service.analyze(target_path)

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
