"""Initialize Flask app."""

import os

from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import cs235flix.adapters.repository as repo
from cs235flix.adapters import database_repository
from cs235flix.adapters import memory_repository
from cs235flix.adapters.memory_repository import MemoryRepository, populate
from cs235flix.adapters.orm import metadata, map_model_to_tables


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('cs235flix', 'adapters', 'data')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

        # Here the "magic" of our repository pattern happens. We can easily switch between in memory data and
        # persistent database data storage for our application.

        if app.config['REPOSITORY'] == 'memory':
            # Create the MemoryRepository instance for a memory-based repository.
            repo.repo_instance = memory_repository.MemoryRepository()
            memory_repository.populate(data_path, repo.repo_instance)

        elif app.config['REPOSITORY'] == 'database':
            # Configure database.
            database_uri = app.config['SQLALCHEMY_DATABASE_URI']

            # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
            # For example the file database could be located locally and relative to the application in covid-19.db,
            # leading to a URI of "sqlite:///covid-19.db".
            # Note that create_engine does not establish any actual DB connection directly!
            database_echo = app.config['SQLALCHEMY_ECHO']
            database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                            echo=database_echo)

            if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
                print("REPOPULATING DATABASE")
                # For testing, or first-time use of the web application, reinitialise the database.
                clear_mappers()
                metadata.create_all(database_engine)  # Conditionally create database tables.
                for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                    database_engine.execute(table.delete())

                # Generate mappings that map domain model classes to the database tables.
                map_model_to_tables()

                database_repository.populate(database_engine, data_path)

            else:
                # Solely generate mappings that map domain model classes to the database tables.
                map_model_to_tables()

            # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
            session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
            # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
            repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    '''
    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)
    '''

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from cs235flix.home import home
        app.register_blueprint(home.home_blueprint)

        from cs235flix.movie import movie
        app.register_blueprint(movie.movie_blueprint)

        from cs235flix.genre import genre
        app.register_blueprint(genre.genre_blueprint)

        from cs235flix.actor import actor
        app.register_blueprint(actor.actor_blueprint)

        from cs235flix.director import director
        app.register_blueprint(director.director_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .watchlist import watchlist
        app.register_blueprint(watchlist.watchlist_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
