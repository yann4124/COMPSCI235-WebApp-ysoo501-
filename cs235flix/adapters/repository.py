import abc
from cs235flix.domain.model import User, Actor, Genre, Movie, Director

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movies(self):
        # Returns all the movies on the app
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movies_by_rank(self):
        # Returns all movies by rank
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_name(self, title, date):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre_by_name(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genre_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_watchlist(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie_to_watchlist(self, user, movie):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_movie_from_watchlist(self, user, movie):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, user, review_text, movie, date, rating):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_movie(self, movie, date):
        raise NotImplementedError

