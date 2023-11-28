"""Movie Index Class."""
import json
import random
import socket
from base64 import b64decode, b64encode
from pathlib import Path
from typing import List

from flask import Flask, flash, render_template_string, request

from movie_index.constants import (ASCII_ENCODING, DEFAULT_IP,
                                   DEFAULT_WEB_PORT, GET, JSON_INDENT,
                                   MOVIE_SOURCES, POST, SECRET_KEY,
                                   UTF8_ENCODING)
from movie_index.util import EnhancedJSONEncoder, File_t

from ._movie import Movie
from ._webpage import (ADD_MOVIE_SUBMIT_VALUE, GEN_RAND_SUBMIT_VALUE,
                       INDEX_PAGE, MOVIE_SOURCE_SELECTION_INPUT,
                       MOVIE_SOURCES_OUTPUT, MOVIE_TITLE_INPUT,
                       SUBMIT_BUTTON_INPUT)


class MovieIndex(Flask):
    UNWATCHED_DATABASE = Path("cache", "unwatched_movies.json")
    WATCHED_DATABASE = Path("cache", "watched_movies.json")

    def __init__(self, *args, **kwargs) -> None:
        """Constructor for MovieIndex.

        Args:
            All Args are passed to flask.Flask constructor.
        """
        super().__init__(*args, **kwargs)

        # Add pages.
        self.add_main_page()

        # Load default config.
        self.movie_list: List[Movie] = []
        self.watched_movies: List[Movie] = []
        self.movie_sources = sorted(MOVIE_SOURCES)

        # Read the movies in if they exist.
        if (
            Path(self.WATCHED_DATABASE).exists()
            and Path(self.UNWATCHED_DATABASE).exists()
        ):
            self._read_movies()

        # Set the session secret.
        self.config["SECRET_KEY"] = SECRET_KEY

    def __del__(self) -> None:
        """Destructor for this flask app.

        Stores the movies into the database.
        """
        self._store_movies()

    @staticmethod
    def host_ip() -> str:
        """Get the host IP.

        Returns:
            The IP for the current host.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((DEFAULT_IP, DEFAULT_WEB_PORT))
        host_ip = s.getsockname()[0]
        s.close()

        return host_ip

    def add_main_page(self) -> None:
        """Add the main flask page."""
        self.add_url_rule("/", view_func=self._index, methods=[GET, POST])

    def _index(self) -> str:
        """Main index page for this flask app.

        On GET: Renders the main page for adding movies to he database.
        On POST: Adds a movie to the database.

        Returns:
            The rendered database to print.
        """
        return_code = 200
        if request.method == POST:
            if request.form.get(SUBMIT_BUTTON_INPUT) == ADD_MOVIE_SUBMIT_VALUE:
                movie_title = self._encode_string(request.form.get(MOVIE_TITLE_INPUT))
                movie_sources = request.form.getlist(MOVIE_SOURCE_SELECTION_INPUT)
                self.movie_list.append(Movie(movie_title, movie_sources))
                self._store_movies()
            elif request.form.get(SUBMIT_BUTTON_INPUT) == GEN_RAND_SUBMIT_VALUE:
                random_movie_index = random.randint(0, len(self.movie_list))
                random_movie = self.movie_list.pop(random_movie_index)

                flash(f"Movie chosen: {self._decode_cipher(random_movie.title)}")
                flash(f"Movie Sources: {', '.join(random_movie.sources)}")

                self.watched_movies.append(random_movie)
            else:
                return_code = 204

        return (
            render_template_string(
                INDEX_PAGE, **{MOVIE_SOURCES_OUTPUT: self.movie_sources}
            ),
            return_code,
        )

    def _store_movies(self) -> None:
        """Store all the movies that we have."""
        self._store_movie_list(self.UNWATCHED_DATABASE, self.movie_list)
        self._store_movie_list(self.WATCHED_DATABASE, self.watched_movies)

    @staticmethod
    def _store_movie_list(database: File_t, movie_list: List[Movie]) -> None:
        """Store the given list of movies into the given JSON database file.

        Args:
            database: The file to store the movie list in.
            movie_list: The list to store.
        """
        Path(database).parent.mkdir(exist_ok=True, parents=True)
        Path(database).write_text(
            json.dumps(movie_list, cls=EnhancedJSONEncoder, indent=JSON_INDENT)
        )

    def _read_movies(self) -> None:
        """Read all the movies from the given database file."""
        self.movie_list = self._read_movie_list(self.UNWATCHED_DATABASE)
        self.watched_movies = self._read_movie_list(self.WATCHED_DATABASE)

    @staticmethod
    def _read_movie_list(database: File_t) -> List[Movie]:
        """Read the given list of movies from the given JSON database file.

        Args:
            database: The file to read the movie list from.
        """
        json_data = json.loads(Path(database).read_text())

        movie_list = []
        for entry in json_data:
            movie_list.append(Movie(**entry))

        return movie_list

    @staticmethod
    def _encode_string(msg: str) -> bytes:
        """Base 64 encode the given ASCII message.

        Args:
            msg: The ASCII message to encode.

        Returns:
            The encoded ASCII message in base64.
        """
        return b64encode(bytes(msg, encoding=ASCII_ENCODING)).decode(
            encoding=UTF8_ENCODING
        )

    @staticmethod
    def _decode_cipher(cipher_text: str) -> str:
        """Base 64 decode the given ASCII cipher.

        Args:
            cipher_text: The ASCII cipher to decode.

        Returns:
            The decoded ASCII message.
        """
        return b64decode(bytes(cipher_text, encoding=ASCII_ENCODING)).decode(
            encoding=UTF8_ENCODING
        )
