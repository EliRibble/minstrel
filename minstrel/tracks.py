import hashlib
import os
import random

import minstrel.db

MUSIC_ROOT = '/music'

class Track():
    def __init__(self, path):
        self.path = path

    def md5(self):
        with open(self.path, 'rb') as f:
            return hashlib.md5(f.read())

    def size(self):
        return os.path.getsize(self.path)

    def url(self):
        return '/track/' + os.path.basename(self.path)

def add_all_to_database():
    tracks = get_all()
    for track in tracks:
        minstrel.db.add_track(track)

def get_all():
    return [Track(os.path.join(MUSIC_ROOT, track)) for track in os.listdir(MUSIC_ROOT) if os.path.isfile(os.path.join(MUSIC_ROOT, track))]

def next_track_for_mood(mood):
    return random.choice(get_all())
