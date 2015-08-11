class MetadataAggregator(object):
    def __init__(self, archive, photo_repo):
        self.archive    = archive
        self.photo_repo = photo_repo
        
    def analyze(self, path):
        amodel = self.archive.open(path)
        entity = amodel.create_entity()

        photo_query = self.photo_repo.new_criteria('p')
        photo_query.expect('p.hashsum = :hashsum')
        photo_query.define('hashsum', entity.hashsum)
        photo_query.limit(1)

        result = self.photo_repo.find(photo_query)

        if result:
            return

        self.photo_repo.persist(entity)
        self.photo_repo.commit()