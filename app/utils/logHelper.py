from fastapi import BackgroundTasks


def write_log(message="", level="info"):
    with open("log.txt", mode="a") as log:
        log.write(f"{level}: {message}\n")


async def log_manager(message="",
                      level="info", background_tasks: BackgroundTasks = None):
    if background_tasks:
        """Log manager function to handle different log levels."""
        background_tasks.add_task(
            write_log, message=message, level=level)
