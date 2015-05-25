from PIL import Image
from PIL import ExifTags

class Photograph(object):
    def __init__(self, location):
        self._location = location
        self._original = None
        self._exif     = None

    def _load(self):
        if self._original:
            return

        self._original = Image.open(self._location)

    @property
    def original(self):
        self._load()

        return self._original

    @property
    def exif(self):
        if self._exif:
            return self._exif

        image    = self.original
        raw_data = image._getexif()

        self._exif = {
            ExifTags.TAGS[k]: raw_data[k]
            for k in raw_data
            if k in ExifTags.TAGS
        }

        return self._exif
