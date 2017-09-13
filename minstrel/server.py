from flask import Flask, render_template, redirect

import minstrel.routes

def create_app():
    app = Flask('minstrel', template_folder='/src/templates')

    app.register_blueprint(minstrel.routes.blueprint)

    return app
