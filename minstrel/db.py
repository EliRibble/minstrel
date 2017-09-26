import logging
import chryso.connection
import chryso.errors
import minstrel.tables

LOGGER = logging.getLogger(__name__)

def add_track(track):
    engine = chryso.connection.get()
    query = minstrel.tables.Track.insert().values(
        md5  = track.md5().hexdigest(),
        size = track.size(),
    )
    try:
        track_id = engine.execute(query).inserted_primary_key[0]
    except chryso.errors.DuplicateKeyError:
        LOGGER.info("Skipping track %s since it is already present", track.path)
        return
    query = minstrel.tables.TrackLocation.insert().values(
        track       = track_id,
        location    = track.path,
    )
    engine.execute(query)
    LOGGER.info("Added track %s with UUID %s", track.path, track_id)

def all_tracks():
    engine = chryso.connection.get()
    query = minstrel.tables.Track.select()
    results = engine.execute(query).fetchall()
    return [dict(row) for row in results]

def all_track_locations():
    engine = chryso.connection.get()
    query = minstrel.tables.TrackLocation.select()
    results = engine.execute(query).fetchall()
    return [dict(row) for row in results]

def all_track_storages():
    engine = chryso.connection.get()
    query = minstrel.tables.TrackStore.select()
    results = engine.execute(query).fetchall()
    return [dict(row) for row in results]

def all_track_locations_for_storage(uuid):
    engine = chryso.connection.get()
    query = minstrel.tables.TrackLocation.select().where(
        minstrel.tables.TrackLocation.c.store == uuid
    )
    results = engine.execute(query).fetchall()
    return [dict(row) for row in results]

def create_play(mood, played_seconds, positive_feedback, track):
    engine = chryso.connection.get()
    query = minstrel.tables.Play.insert().values(
        mood                = mood,
        played_seconds      = played_seconds,
        positive_feedback   = positive_feedback,
        track               = track,
    )
    play_id = engine.execute(query).inserted_primary_key[0]
    LOGGER.debug("Created play %s", play_id)
    return play_id

def get_plays():
    engine = chryso.connection.get()
    query = minstrel.tables.Play.select()
    return [dict(row) for row in engine.execute(query).fetchall()]

def get_track(uuid):
    engine = chryso.connection.get()
    query = minstrel.tables.Track.select().where(
        minstrel.tables.Track.c.uuid == uuid
    )
    results = engine.execute(query).fetchone()
    return dict(results)

def get_track_location(storage=None, track=None, uuid=None):
    engine = chryso.connection.get()
    query = minstrel.tables.TrackLocation.select()
    if uuid:
        query = query.where(
            minstrel.tables.TrackLocation.c.track == uuid
        )
    elif storage and track:
        query = query.where(
            minstrel.tables.TrackLocation.c.store == storage,
        ).where(
            minstrel.tables.TrackLocation.c.track == track,
        )
    else:
        raise Exception('you should provide either storage and track or uuid')
    results = engine.execute(query).fetchone()
    return dict(results)

def get_track_storage(name):
    engine = chryso.connection.get()
    query = minstrel.tables.TrackStore.select().where(
        minstrel.tables.TrackStore.c.name == name
    )
    results = engine.execute(query).fetchone()
    return dict(results)

def reinforce(track_uuid, positive=True):
    engine = chryso.connection.get()
    #query = minstrel.tables.

def set_mood(mood):
    engine = chryso.connection.get()
    query = minstrel.tables.State.update().values(mood=mood)
    engine.execute(query)

def get_mood():
    engine = chryso.connection.get()
    query = minstrel.tables.State.select()
    return engine.execute(query).fetchone()[minstrel.tables.State.c.mood]
