import hashlib
from PIL import Image
from PIL import ExifTags
from photos.entity import Photography as P

class Photograph(object):
    exif_tag_to_attribute_map = {
        'ExifImageHeight':       'height',
        'ExifImageWidth':        'width',
        'ExposureTime':          'exposure_time',
        'FNumber':               'aperture',
        'Flash':                 'flash',
        'FocalLength':           'focal_length',
        'FocalLengthIn35mmFilm': 'focal_length_35mm',
        'ISOSpeedRatings':       'iso',
        'Make':                  'manufacture',
        'MeteringMode':          'metering_mode',
        'Model':                 'model',
        'Orientation':           'orientation',
        'WhiteBalance':          'white_balance',
        'DateTime':              'date_time',
    }

    exif_tag_maker_note = 'MakerNote'

    def __init__(self, location, exif=None, hashsum=None):
        self._original = None
        self._content  = None

        self.location = location
        self._exif    = exif
        self._hashsum = hashsum

    def original(self):
        if not self._original:
            self._original = Image.open(self.location)

        return self._original

    def content(self):
        if not self._content:
            with open(self.location, 'rb') as f:
                self._content = f.read()

        return self._content

    def info(self, *keys):
        labels = self.exif_tag_to_attribute_map
        exif   = self.exif

        return {
            labels[k]: exif[k]
            for k in labels
            if (not keys or k in keys) and k in exif
        }

    @property
    def hashsum(self):
        if not self._hashsum:
            m = hashlib.new('sha1')
            m.update(self.content())

            self._hashsum = m.hexdigest()

        return self._hashsum

    @hashsum.setter
    def hashsum(self, value):
        self._hashsum = value

    @property
    def exif(self):
        if self._exif:
            return self._exif

        image    = self.original()
        raw_data = image._getexif()

        self._exif = {
            ExifTags.TAGS[k]: raw_data[k]
            for k in raw_data
            if k in ExifTags.TAGS
        }

        return self._exif

    @exif.setter
    def exif(self, value):
        self._exif = value

    def create_entity(self):
        width, height = self.original().size

        info = self.info()

        # Override the dimension.
        info['width']  = width
        info['height'] = height

        # Rewrite the data.
        if 'aperture' in info:
            info['original_aperture'] = info['aperture']
            info['aperture']          = float(info['aperture'][0]) / info['aperture'][1]

        if 'focal_length' in info:
            info['original_focal_length'] = info['focal_length']
            info['focal_length']          = float(info['focal_length'][0]) / info['focal_length'][1]

        if 'exposure_time' in info:
            info['original_exposure_time'] = info['exposure_time']

            if info['exposure_time'][0] > info['exposure_time'][1]:
                info['exposure_time'] = str(info['exposure_time'][0])
            else:
                info['exposure_time'] = '{}/{}'.format(info['exposure_time'][0], info['exposure_time'][1])

        return P(
            location = self.location,
            hashsum  = self.hashsum,
            **info
        )

    def _load_image(self):
        if self._original:
            return

        self._original = Image.open(self.location)
