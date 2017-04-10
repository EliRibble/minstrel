import minstrel.server

def run(debug=True):
    app = minstrel.server.create_app()
    app.run('localhost', 8000, debug=debug)
