from fastapi import FastAPI
from app.routers import slpkRouter  # Import the routers
from fastapi.middleware.cors import CORSMiddleware
import re
from starlette.routing import Route
from app.utils.cacheHelper import cache_start_up

app = FastAPI(lifespan=cache_start_up)  # Initialize FastAPI with cache startup

origins = [
    "*",
]
# Allows all origins, you can specify a list of allowed origins here
# Set up CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include the router
app.include_router(slpkRouter.router)
for route in app.router.routes:
    if isinstance(route, Route):
        route.path_regex = re.compile(route.path_regex.pattern, re.IGNORECASE)
