"""Data structure for one movie."""
from typing import List
from dataclasses import dataclass

@dataclass
class Movie:
    title: str  # The title of thid movie.
    sources: List[str]  # The list of places this movie can be watched from.
