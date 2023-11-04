"""Main entry point for this application."""
from movie_index.app import MovieIndex

def main():
    """Main entry Point"""
    app = MovieIndex(__name__)
    app.run(host=app.host_ip())

if __name__ == "__main__":
    main()
