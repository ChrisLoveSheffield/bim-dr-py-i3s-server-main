from fastapi_cache.decorator import cache
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


@asynccontextmanager
async def cache_start_up(_):
    FastAPICache.init(InMemoryBackend(), prefix="slpk-cache")
    print("Cache initialized with InMemoryBackend")
    yield  # This is where the app runs
    # Perform shutdown tasks (e.g., clean up cache)
    print("Shutting down...")
    # from main import home


cache = cache
