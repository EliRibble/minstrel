import flask
import logging

import minstrel.tracks

LOGGER = logging.getLogger(__name__)

blueprint = flask.Blueprint('routes', __name__)

MOOD = None

@blueprint.route('/')
def index():
    tracks = minstrel.tracks.get_all()
    return flask.render_template('root.html', tracks=tracks)

@blueprint.route('/favicon.ico')
def favicon():
    return flask.send_from_directory('/src/static/', 'favicon.ico')

@blueprint.route('/mood/', methods=['POST'])
def mood_post():
    global MOOD
    MOOD = flask.request.form['mood']
    LOGGER.info("Got a new mood of %s", MOOD)
    track = minstrel.tracks.next_track_for_mood(MOOD)
    return flask.redirect(track.url())

@blueprint.route('/next/', methods=['GET', 'POST'])
def next_track():
    next_track = minstrel.tracks.next_track_for_mood(MOOD)
    return flask.redirect(next_track.url())

@blueprint.route('/music/<path:path>/')
def send_music(path):
    return flask.send_from_directory('/music/', path)

@blueprint.route('/track/<uuid>/')
def track(uuid):
    _track = minstrel.tracks.get(uuid)
    return flask.render_template('track.html', mood=MOOD, track=_track)

