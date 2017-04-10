import flask

blueprint = flask.Blueprint('routes', __name__)

@blueprint.route('/')
def index():
    return flask.render_template('root.html')
