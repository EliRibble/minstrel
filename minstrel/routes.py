import flask
import logging

import minstrel.db
import minstrel.tracks

LOGGER = logging.getLogger(__name__)

blueprint = flask.Blueprint('routes', __name__)

@blueprint.route('/')
def index():
    tracks = minstrel.tracks.get_all()
    return flask.render_template('root.html', tracks=tracks)

@blueprint.route('/favicon.ico')
def favicon():
    return flask.send_from_directory('/src/static/', 'favicon.ico')

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

@blueprint.route('/music/<path:path>/')
def send_music(path):
    return flask.send_from_directory('/music/', path)

@blueprint.route('/track/<uuid>/')
def track(uuid):
    mood = minstrel.db.get_mood()
    _track = minstrel.tracks.get(uuid)
    return flask.render_template('track.html', mood=mood, track=_track)

