import re
import sys
from photos.archive import Archive

location = sys.argv[1]

archive = Archive()
photo   = archive.open(location)

import pprint

pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(photo.exif.keys())

print('Location:  {}'.format(photo.location))
print('SHA1 Hash: {}'.format(photo.hashsum))

info = photo.info()

for l in info:
    v = info[l]
    print(' | {:>30}: {}'.format(l, v))

#print('MakerNote: {}'.format(photo.exif['MakerNote']))

#maker_note = photo.exif['MakerNote']

# for c in maker_note:
#     print(ord(c))

# raw_data = photo.original._getexif()
# 
# exif = {
#     k: raw_data[k]
#     for k in raw_data
# }
# 
# pp.pprint(exif)
