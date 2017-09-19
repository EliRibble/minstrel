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

def get_track_location(uuid):
    engine = chryso.connection.get()
    query = minstrel.tables.TrackLocation.select().where(
        minstrel.tables.TrackLocation.c.track == uuid
    )
    results = engine.execute(query).fetchone()
    return dict(results)
