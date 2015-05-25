import sys
from photos.archive import Archive

location = sys.argv[1]

archive = Archive()
photo   = archive.open(location)

import pprint

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(photo.exif.keys())
