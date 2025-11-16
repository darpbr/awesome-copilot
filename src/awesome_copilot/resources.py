from typing import Dict, Any
from functools import lru_cache


# Aqui você encapsula clientes de banco, caches e conexões externas.


class InMemoryStore:
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def get(self, key: str):
        return self._store.get(key)

    def set(self, key: str, value: Any):
        self._store[key] = value


@lru_cache()
def get_resources() -> dict:
    return {
        "store": InMemoryStore(),
    }
