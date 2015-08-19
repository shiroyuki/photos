from photos.active_model import Photograph as P

class Archive(object):
    def open(self, location):
        return P(location)
