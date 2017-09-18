import logging

import alembic.command
import alembic.config
import chryso.connection
import minstrel.server
import minstrel.tables

LOGGER = logging.getLogger(__name__)

def connect_db():
    engine = chryso.connection.Engine('postgres://postgres@db:5432/postgres', minstrel.tables)
    chryso.connection.store(engine)
    logging.getLogger('chryso.connection.PoolForThreads').setLevel(logging.INFO)

def run(debug=True):
    logging.basicConfig(level=logging.DEBUG)

    connect_db()
    app = minstrel.server.create_app()
    run_alembic()
    app.run('0.0.0.0', 8000, debug=debug)

def run_alembic():
    LOGGER.info("Running alembic to upgrade to the latest DB schema")
    config = alembic.config.Config(file_='/etc/minstrel/alembic.ini', ini_section='alembic', cmd_opts=None)
    alembic.command.upgrade(config, revision='head', sql=False, tag=None)
    LOGGER.info("Alembic run complete")
