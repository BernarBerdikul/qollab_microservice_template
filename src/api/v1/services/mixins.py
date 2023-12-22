from dataclasses import dataclass

from src.db import dummy_cache
from src.db.cache import AbstractCache
from src.repositories import AbstractRepository


@dataclass
class ServiceMixin:
    cache: AbstractCache
    repository: AbstractRepository

    def __post_init__(self):
        if self.cache is None:
            self.cache = dummy_cache.DummyCache()
