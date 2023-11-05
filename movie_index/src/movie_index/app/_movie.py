"""Data structure for one movie."""
from typing import List
from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    sources: List[str]
