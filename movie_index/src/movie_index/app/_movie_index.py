"""Movie Index Class."""

from flask import Flask, render_template_string, request
import socket

from ._webpage import WEBPAGE

class MovieIndex(Flask):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_main_page()

        self.movie_list = []
        self.movie_sources = []

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
        self.add_url_rule("/", view_func=self._index, methods=["GET", "POST"])

    @staticmethod
    def _index() -> str:
        """Main index page for this flask app."""
        if request.method == 'POST':
            pass

        return render_template_string(WEBPAGE)
