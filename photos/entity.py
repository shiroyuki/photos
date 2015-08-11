from passerine.db.entity import entity

@entity('photographs')
class Photography(object):
    def __init__(
        self,
        location,
        hashsum,
        height              = None,
        width               = None,
        exposure_time       = None,
        aperture            = None,
        flash               = None,
        focal_length        = None,
        focal_length_35mm   = None,
        iso                 = None,
        manufacture         = None,
        metering_mode       = None,
        model               = None,
        orientation         = None,
        white_balance       = None,
        date_time           = None,
        original_aperture      = None,
        original_focal_length  = None,
        original_exposure_time = None
    ):
        self.location          = location
        self.hashsum           = hashsum
        self.height            = height
        self.width             = width
        self.exposure_time     = exposure_time
        self.aperture          = aperture
        self.flash             = flash
        self.focal_length      = focal_length
        self.focal_length_35mm = focal_length_35mm
        self.iso               = iso
        self.manufacture       = manufacture
        self.metering_mode     = metering_mode
        self.model             = model
        self.orientation       = orientation
        self.white_balance     = white_balance
        self.date_time         = date_time
        self.original_aperture      = original_focal_length
        self.original_focal_length  = original_exposure_time
        self.original_exposure_time = original_aperture

class AG_Aperture(object):
    def __init__(self, aperture):
        self.aperture = aperture

class AG_ISO(object):
    def __init__(self, iso):
        self.iso = iso

class AG_Aperture(object):
    def __init__(self, aperture):
        self.aperture = aperture

class AG_ISO(object):
    def __init__(self, iso):
        self.iso = iso
