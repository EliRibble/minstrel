import hashlib
import logging
import os
import random

import minstrel.db

LOGGER = logging.getLogger(__name__)
MUSIC_ROOT = '/music'

class Track():
    def __init__(self, path, uuid):
        self.path   = path
        self.uuid   = uuid

    def md5(self):
        with open(self.path, 'rb') as f:
            return hashlib.md5(f.read())

    def size(self):
        return os.path.getsize(self.path)

    def url(self):
        return '/track/' + str(self.uuid)

def add_all_to_database():
    tracks = [Track(
        path    = os.path.join(MUSIC_ROOT, track),
        uuid    = None,
    ) for track in os.listdir(MUSIC_ROOT) if os.path.isfile(os.path.join(MUSIC_ROOT, track))]
    for track in tracks:
        minstrel.db.add_track(track)

def get(uuid):
    location = minstrel.db.get_track_location(uuid)
    return Track(
        path    = location['location'],
        uuid    = location['track'],
    )

def get_all():
    locations = minstrel.db.all_track_locations()
    return [Track(
        path    = location['location'],
        uuid    = location['track'],
    ) for location in locations]

def played(mood, played_seconds, positive_feedback, track):
    LOGGER.info("Played track %s for %s seconds on mood %s with positive feedback %s", track, played_seconds, mood, positive_feedback)
    minstrel.db.create_play(
        mood                = mood,
        played_seconds      = played_seconds,
        positive_feedback   = positive_feedback,
        track               = track,
    )

def next_track_for_mood(mood):
    return random.choice(get_all())

def reinforce(track_uuid, positive=True):
    minstrel.db.reinforce(track_uuid, positive=positive)
