import logging

import alembic.command
import alembic.config

import minstrel.server

LOGGER = logging.getLogger(__name__)

def run(debug=True):
    app = minstrel.server.create_app()
    run_alembic()
    app.run('0.0.0.0', 8000, debug=debug)

def run_alembic():
    LOGGER.info("Running alembic to upgrade to the latest DB schema")
    config = alembic.config.Config(file_='/etc/minstrel/alembic.ini', ini_section='alembic', cmd_opts=None)
    alembic.command.upgrade(config, revision='head', sql=False, tag=None)
    LOGGER.info("Alembic run complete")
