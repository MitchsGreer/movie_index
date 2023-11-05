"""Data structure for one movie."""
from dataclasses import dataclass
from typing import List


@dataclass
class Movie:
    title: str  # The title of thid movie.
    sources: List[str]  # The list of places this movie can be watched from.
