import os
import random

MUSIC_ROOT = '/music'

class Track():
    def __init__(self, path):
        self.path = path

    def url(self):
        return '/track/' + os.path.basename(self.path)

def get_all():
    return [Track(os.path.join(MUSIC_ROOT, track)) for track in os.listdir(MUSIC_ROOT) if os.path.isfile(os.path.join(MUSIC_ROOT, track))]

def next_track_for_mood(mood):
    return random.choice(get_all())
