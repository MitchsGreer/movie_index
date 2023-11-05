"""Movie Index Class.

TODO:
    - Add title mangling so they are not shown in the database.
"""
from typing import List
import socket
import json
from pathlib import Path
from base64 import encode, decode

from flask import Flask, render_template_string, request

from movie_index.util import File_t, EnhancedJSONEncoder
from ._movie import Movie

from ._webpage import (
    WEBPAGE,
    MOVIE_TITLE_INPUT,
    MOVIE_SOURCE_SELECTION_INPUT,
    SUBMIT_BUTTON_INPUT
)

class MovieIndex(Flask):
    POST = "POST"
    GET = "GET"
    JSON_DATABASE = Path("cache", "database.json")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_main_page()

        self.movie_list: List[Movie] = []
        self.movie_sources = sorted(
            [
                "Amazon Prime",
                "Apple TV",
                "Netflix",
                "Peacock",
                "Max",
                "Hulu",
                "Disney+"
            ]
        )

        if Path(self.JSON_DATABASE).exists():
            self._read_movies(self.JSON_DATABASE)

    def __del__(self) -> None:
        """Destructor for this flask app."""
        self._store_movies(self.JSON_DATABASE)

    @staticmethod
    def host_ip() -> str:
        """Get the host IP."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host_ip = s.getsockname()[0]
        s.close()

        return host_ip

    def add_main_page(self) -> None:
        """Add the main flask page."""
        self.add_url_rule("/", view_func=self._index, methods=[MovieIndex.GET, MovieIndex.POST])

    def _index(self) -> str:
        """Main index page for this flask app."""
        if request.method == MovieIndex.POST:
            movie_title = request.form.get(MOVIE_TITLE_INPUT)
            movie_sources = request.form.getlist(MOVIE_SOURCE_SELECTION_INPUT)

            self.movie_list.append(
                Movie(movie_title, movie_sources)
            )

        return render_template_string(
            WEBPAGE,
            **{
                "movie_sources": self.movie_sources
            }
        )

    def _store_movies(self, database: File_t) -> None:
        """Store all the movies that we have.

        Arguments:
            database: The file to save the movie data to.
        """
        Path(self.JSON_DATABASE).parent.mkdir(exist_ok=True, parents=True)
        Path(database).write_text(json.dumps(self.movie_list, cls=EnhancedJSONEncoder))

    def _read_movies(self, database: File_t) -> None:
        """Read all the movies from the given database file.

        Arguments:
            database: The file to read the movie data from.
        """
        json_data = json.loads(Path(database).read_text())

        for entry in json_data:
            self.movie_list.append(Movie(**entry))

    @staticmethod
    def _encode_title(title: str) -> str:
        """Base 64 encode the given title."""
        return encode(title)
