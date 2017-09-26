import flask
import logging

import minstrel.db
import minstrel.tracks
import minstrel.storage

LOGGER = logging.getLogger(__name__)

blueprint = flask.Blueprint('routes', __name__)

@blueprint.route('/')
def index():
    tracks = []
    return flask.render_template('root.html', tracks=tracks)

@blueprint.route('/favicon.ico')
def favicon():
    return flask.send_from_directory('/src/static/', 'favicon.ico')

@blueprint.route('/history/', methods=['GET'])
def history():
    plays = minstrel.tracks.get_plays()
    return flask.render_template('history.html', plays=plays)

@blueprint.route('/mood/', methods=['POST'])
def mood_post():
    mood = flask.request.form['mood']
    LOGGER.info("Got a new mood of %s", mood)
    minstrel.db.set_mood(mood)
    track = minstrel.tracks.next_track_for_mood(mood)
    return flask.redirect(track.url())

@blueprint.route('/next/', methods=['GET', 'POST'])
def next_track():
    mood = minstrel.db.get_mood()
    if flask.request.method == 'POST':
        LOGGER.debug("current time at next %s", flask.request.form['currentTime'])
        minstrel.tracks.played(
            mood                = mood,
            played_seconds      = flask.request.form['currentTime'],
            positive_feedback   = None,
            track               = flask.request.form['track'],
        )
    next_track = minstrel.tracks.next_track_for_mood(mood)
    return flask.redirect(next_track.url())

@blueprint.route('/content/<path:path>/')
def send_music(path):
    return flask.send_from_directory('/music/', path)

@blueprint.route('/track/')
def tracks():
    storages = minstrel.storage.get_all()
    tracks = set()
    for storage in storages:
        for track_location in storage.track_locations:
            tracks.add(track_location.track)
    return flask.render_template('tracks.html', storages=storages, tracks=tracks)

@blueprint.route('/track/<uuid>/')
def track(uuid):
    mood = minstrel.db.get_mood()
    cloud = minstrel.storage.get('cloud')
    cloud_location = minstrel.tracks.get_location(
        storage = cloud.uuid,
        track   = uuid,
    )
    return flask.render_template('track.html', mood=mood, track_location=cloud_location)

