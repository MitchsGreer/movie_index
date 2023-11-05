"""Main entry point for this application."""
from movie_index.app import MovieIndex
from movie_index.constants import APP_NAME


def main():
    """Main entry Point"""
    app = MovieIndex(APP_NAME)
    app.run(host=app.host_ip())


if __name__ == "__main__":
    main()
