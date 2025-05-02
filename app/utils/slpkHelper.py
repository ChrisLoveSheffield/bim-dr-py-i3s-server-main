
import os
import asyncio
import gzip
import zipfile
from io import BytesIO
from pathlib import Path
from app.config.var import home
# import aiofiles
# from app.utils.cacheHelper import cache
# from main import home


async def read_slpk(f, slpk):
    loop = asyncio.get_event_loop()
    slpk_path = os.path.join(home, slpk)

    def read_from_zip():
        with open(slpk_path, 'rb') as file:
            with zipfile.ZipFile(file) as zip:
                if os.path.splitext(f)[1] == ".gz":  # Unzip GZ
                    gz = BytesIO(zip.read(f.replace("\\", "/")))
                    with gzip.GzipFile(fileobj=gz) as gzfile:
                        return gzfile.read()
                else:
                    return zip.read(f.replace("\\", "/"))  # Direct read

    return await loop.run_in_executor(None, read_from_zip)


# @cache(expire=3600)
async def read_eslpk(f, slpk):
    loop = asyncio.get_event_loop()
    eslpk_path = os.path.join(home, slpk)
    f_path = Path(eslpk_path, f)

    def read_file():
        if os.path.splitext(f_path)[1] == ".gz":
            with gzip.open(f_path, 'rb') as gzfile:
                return gzfile.read()
        else:
            with open(f_path, 'rb') as file:
                return file.read()

    return await loop.run_in_executor(None, read_file)


async def read(f, slpk):
    """Read gz compressed file from slpk (=zip archive) and output result.

    Args:
        f (str): File path inside the SLPK archive.
        slpk (str): Name of the SLPK file (Scene Layer Package).
    """
    if f.startswith("\\"):  # Remove first backslash
        f = f[1:]
    if slpk.endswith('.eslpk'):
        return await read_eslpk(f, slpk)
    else:
        return await read_slpk(f, slpk)
