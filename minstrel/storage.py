import minstrel.db
import minstrel.tracks

class TrackStorage():
    def __init__(self, name, track_locations, uuid, created=None, deleted=None, updated=None):
        self.created         = created
        self.name            = name
        self.track_locations = track_locations
        self.updated         = updated
        self.uuid            = uuid

    def get_tracks(self):
        return minstrel.db.all_tracks_for_storage(self.uuid)

def get(name):
    storage = minstrel.db.get_track_storage(name=name)
    return TrackStorage(track_locations=[], **storage)

def get_all():
    tracks = minstrel.tracks.get_all_locations()
    results = [TrackStorage(
        name            = row['name'],
        track_locations = [track for track in tracks if track.store == row['uuid']],
        uuid            = row['uuid'],
    ) for row in minstrel.db.all_track_storages()]
    return results
