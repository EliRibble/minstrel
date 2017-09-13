import flask
import os

blueprint = flask.Blueprint('routes', __name__)

@blueprint.route('/')
def index():
    music = [track for track in os.listdir('/music') if os.path.isfile('/music/' + track)]
    return flask.render_template('root.html', music=music)

@blueprint.route('/track/<filename>/')
def track(filename):
    return flask.render_template('track.html', filename=filename)

@blueprint.route('/music/<path:path>/')
def send_music(path):
    return flask.send_from_directory('/music/', path)
