from fastapi import HTTPException


def abort(code=500, msg='not found'):
    raise HTTPException(status_code=code, detail=msg)
