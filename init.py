
import sys
import os
import argparse
# from pydantic_settings import SettingsConfigDict
from functools import lru_cache
from dotenv import dotenv_values
# from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@lru_cache
def get_settings():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(os.path.abspath(__file__))

    DOTENV = os.path.join(application_path, ".env")
    # load_dotenv(DOTENV)
    config = dotenv_values(DOTENV)
    port = int(config.get("PORT", 8000))
    # Default to 8000 if "port" is not in the dictionary
    workers = int(config.get("WORKER_THREADS", 8))  # Default to 8
    reload_flag = str(config.get("RELOAD")).lower() in (
        'true', '1', 't')  # Default to False
    target = config.get("SLPK_DIR", None)  # Default to None
    return port, workers, reload_flag, target


port, workers, reload_flag, target = get_settings()
slpk_dir = target


def active_argparse():
    parser = argparse.ArgumentParser(description='i3s server')
    parser.add_argument('--port', type=int, default=port,
                        help='Port to run the server on')

    args, unknown = parser.parse_known_args()
    return args.port


if __name__ == '__main__':
    import uvicorn
    import multiprocessing
    # Add the project root to sys.path
    # Default to None

    from app.main import app  # cannot removed this import
    app.title = "i3s server"
    arg_port = active_argparse()
    multiprocessing.freeze_support()
    uvicorn.run("app.main:app",
                port=arg_port, workers=workers, reload=reload_flag,)
    # uvicorn.run(app,,
    #             port=8000)
    sys.exit(0)  # Exit the script after running the server
    pass
