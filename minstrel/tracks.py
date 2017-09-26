import eyed3
import hashlib
import logging
import os
import random
import urllib.parse
import uuid

import minstrel.db

LOGGER = logging.getLogger(__name__)
MUSIC_ROOT = '/music'

class Track():
    def __init__(self, md5, size, uuid, created=None, deleted=None, updated=None):
        self.md5    = md5
        self.size   = size
        self.uuid   = uuid

    def url(self):
        return '/track/{}/'.format(self.uuid)

class TrackLocation():
    def __init__(self, location, store, track, uuid, created=None, deleted=None, updated=None):
        self._audiofile = None
        self.location  = location
        self.store = store
        self.track = track
        self.uuid  = uuid

    @property
    def artist(self):
        return self.audiofile.tag.artist

    @property
    def audiofile(self):
        if not self._audiofile:
            self._audiofile = eyed3.load(self.location)
        return self._audiofile

    @property
    def length(self):
        return self.audiofile.info.time_secs

    def stream_url(self):
        basename = os.path.basename(self.location)
        return urllib.parse.quote('/content/{}'.format(basename))

    @property
    def title(self):
        return self.audiofile.tag.title

def add_all_to_database():
    tracks = [Track(
        path    = os.path.join(MUSIC_ROOT, track),
        uuid    = None,
    ) for track in os.listdir(MUSIC_ROOT) if os.path.isfile(os.path.join(MUSIC_ROOT, track))]
    for track in tracks:
        minstrel.db.add_track(track)

def get(uuid):
    track = minstrel.db.get_track(uuid)
    return Track(
        md5     = track['md5'],
        size    = track['size'],
        uuid    = track['uuid'],
    )

def get_all():
    tracks = minstrel.db.all_tracks()
    return [Track(**track) for track in tracks]

def get_location(storage, track):
    track_ = get(track)
    location = minstrel.db.get_track_location(
        storage = storage,
        track   = track,
    )
    return TrackLocation(
        location    = location['location'],
        store       = location['store'],
        track       = track_,
        uuid        = location['uuid'],
    )

def get_all_locations():
    locations = minstrel.db.all_track_locations()
    tracks = {row['uuid']: Track(
        row['md5'],
        row['size'],
        row['uuid'],
    ) for row in minstrel.db.all_tracks()}
    return [TrackLocation(
        location    = location['location'],
        store       = location['store'],
        track       = tracks[location['track']],
        uuid        = location['uuid'],
    ) for location in locations]

def played(mood, played_seconds, positive_feedback, track):
    LOGGER.info("Played track %s for %s seconds on mood %s with positive feedback %s", track, played_seconds, mood, positive_feedback)
    minstrel.db.create_play(
        mood                = mood,
        played_seconds      = played_seconds,
        positive_feedback   = positive_feedback,
        track               = uuid.UUID(track),
    )

def next_track_for_mood(mood):
    return random.choice(get_all())

def reinforce(track_uuid, positive=True):
    minstrel.db.reinforce(track_uuid, positive=positive)

def get_plays():
    plays = minstrel.db.get_plays()
    tracks = get_all()
