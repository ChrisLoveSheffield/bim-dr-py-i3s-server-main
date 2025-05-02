
from app.utils import abortHelper, responseHelper, slpkHelper, cacheHelper
from fastapi import APIRouter, Request
from functools import wraps
import json
from fastapi.responses import StreamingResponse, RedirectResponse
from io import BytesIO
import os
from app.config.var import home

# Initialize router
router = APIRouter()
cache_expire = 60*10

cache = cacheHelper.cache
abort = abortHelper.abort
HTTPResponse = responseHelper.HTTPResponse
read = slpkHelper.read
slpks = []


def create_slpk_folder_if_not_exists(path):
    """Create the folder if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def update_slpk_list():
    """Update the list of SLPK files."""
    global slpks
    slpks = [f for f in os.listdir(home) if
             #  f.lower().endswith('.slpk') or
             f.lower().endswith('.eslpk')]


create_slpk_folder_if_not_exists(home)
update_slpk_list()


def stringify_response(func):
    """Convert the HTTPResponse object to a string."""
    @wraps(func)
    async def _wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        if isinstance(response, HTTPResponse):
            return response.toJSON()
        return response
    _wrapper.__name__ = func.__name__
    return _wrapper


@router.get('/')
async def redirect_docs():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs")

# @router.get("/")
# async def read_item():
#     return {"item_id": "hello"}


# @router.get("/example")
# @cache(expire=60)  # Cache the response for 60 seconds
# async def example_endpoint():
#     return {"message": "This is a cached response"}


@router.get('/refresh')
@stringify_response
async def refresh_slpk_list():
    """Refresh the list of SLPK files."""
    global slpks
    update_slpk_list()
    return HTTPResponse(body=slpks)


@router.get('/getlist')
@cache(expire=cache_expire)
@stringify_response
async def list_services(request: Request):
    """ List all available SLPK, with LINK to I3S service and Viewer page"""
    # return {"message": "Hello, FastAPI!"}
    print(request)
    url_list = [f'{request.base_url}{slpk}/SceneServer/' for slpk in slpks]
    return HTTPResponse(body=url_list)


@router.get('/{slpk}/SceneServer')
@router.get('/{slpk}/SceneServer/')
@cache(expire=cache_expire)
@stringify_response
async def service_info(slpk):
    """ Service information JSON """
    if slpk not in slpks:  # Get 404 if slpk doesn't exists
        abort(404, "Can't found SLPK: %s" % slpk)
    SceneServiceInfo = dict()
    SceneServiceInfo["serviceName"] = slpk
    SceneServiceInfo["name"] = slpk
    SceneServiceInfo["currentVersion"] = 10.6
    SceneServiceInfo["serviceVersion"] = "1.6"
    SceneServiceInfo["supportedBindings"] = ["REST"]
    SceneServiceInfo["layers"] = [
        json.loads(await read("3dSceneLayer.json.gz", slpk))]

    return HTTPResponse(body=SceneServiceInfo,
                        content_type='application/json')


@router.get('/{slpk}/SceneServer/layers/0')
@router.get('/{slpk}/SceneServer/layers/0/')
@cache(expire=cache_expire)
@stringify_response
async def layer_info(slpk):
    """ Layer information JSON """
    if slpk not in slpks:  # Get 404 if slpk doesn't exists
        abort(404, "Can't found SLPK: %s" % slpk)
    SceneLayerInfo = json.loads(
        await read("3dSceneLayer.json.gz", slpk))
    return HTTPResponse(body=SceneLayerInfo,
                        content_type='application/json')


@router.get('/{slpk}/SceneServer/layers/{layer}/nodepages')
@router.get('/{slpk}/SceneServer/layers/{layer}/nodepages/')
@cache(expire=cache_expire)
@stringify_response
async def node_info(slpk, layer):
    NodeIndexDocument = json.loads(
        await read(
            "nodepages/0.json.gz", slpk
        ))
    return HTTPResponse(body=NodeIndexDocument,
                        content_type='application/json')


@router.get('/{slpk}/SceneServer/layers/{layer}/nodepages/{node}')
@router.get('/{slpk}/SceneServer/layers/{layer}/nodepages/{node}/')
@cache(expire=cache_expire)
@stringify_response
async def node_pages_info(slpk, layer, node):
    """ Node information JSON """
    NodeIndexDocument = json.loads(
        await read(f"nodepages/{node}.json.gz", slpk))
    return HTTPResponse(body=NodeIndexDocument,
                        content_type='application/json')


@router.get(
    (
        '/{slpk}/SceneServer/layers/{layer}/nodes/{node}/geometries/'
        '{geometry_id}'
    )
)
@router.get(
    (
        '/{slpk}/SceneServer/layers/{layer}/nodes/{node}/geometries/'
        '{geometry_id}/'
    )
)
async def geometry_info(slpk, layer, node, geometry_id):
    """ Geometry information bin """
    if slpk not in slpks:  # Get 404 if slpk doesn't exists
        abort(404, "Can't found SLPK: %s" % slpk)
    content = await read("nodes/%s/geometries/%s.bin.gz" %
                         (node, geometry_id), slpk, )
    if not content:
        abort(404, "Can't found content: %s" % slpk)
    # todo: update to cus http response
    response = StreamingResponse(
        BytesIO(content),
        media_type="application/octet-stream; charset=binary"
    )
    return response


@router.get('/{slpk}/SceneServer/layers/{layer}/nodes/{node}/textures/0_0')
@router.get('/{slpk}/SceneServer/layers/{layer}/nodes/{node}/textures/0_0/')
async def textures_info(slpk, layer, node):
    """ Texture information JPG """
    if slpk not in slpks:  # Get 404 if slpk doesn't exists
        abort(404, "Can't found SLPK: %s" % slpk)

    try:
        content = await read("nodes/%s/textures/0_0.jpg" % node, slpk)
    except Exception:
        try:
            content = await read("nodes/%s/textures/0_0.bin" % node, slpk)
        except Exception:
            content = ""
    finally:
        if content == "":
            abort(404, "Can't found content: %s" % slpk)
        else:
            response = StreamingResponse(
                BytesIO(content
                        ), media_type='image/jpeg')
            response.headers['Content-Disposition'] = (
                'attachment; filename="0_0.jpg"'
            )
            return response


@router.get('/{slpk}/SceneServer/layers/{layer}/nodes/{node}/textures/0_0_1')
@router.get('/{slpk}/SceneServer/layers/{layer}/nodes/{node}/textures/0_0_1/')
async def Ctextures_info(slpk, layer, node):
    """ Compressed texture information """
    if slpk not in slpks:  # Get 404 if slpk doesn't exists
        abort(404, "Can't found SLPK: %s" % slpk)
    try:
        return await read("nodes/%s/textures/0_0_1.bin.dds.gz" % node, slpk)
    except Exception as e:
        print(e)
        return abort(404, "Can't found content: %s" % slpk)


@router.get('/{slpk}/SceneServer/layers/{layer}/nodes/{node}/features/0')
@router.get('/{slpk}/SceneServer/layers/{layer}/nodes/{node}/features/0/')
@stringify_response
@cache(expire=cache_expire)
async def feature_info(slpk, layer, node):
    """ Feature information JSON """
    if slpk not in slpks:  # Get 404 if slpk doesn't exists
        abort(404, "Can't found SLPK: %s" % slpk)
    print("%s")
    FeatureData = json.loads(
        await read("nodes/%s/features/0.json.gz" % node, slpk))
    response = HTTPResponse(FeatureData)
    return response


@router.get('/{slpk}/SceneServer/layers/{layer}/nodes/{node}/shared')
@router.get('/{slpk}/SceneServer/layers/{layer}/nodes/{node}/shared/')
@cache(expire=cache_expire)
@stringify_response
async def shared_info(slpk, layer, node):
    """ Shared node information JSON """
    if slpk not in slpks:  # Get 404 if slpk doesn't exists
        abort(404, "Can't found SLPK: %s" % slpk)
    try:
        Sharedressource = json.loads(
            await read("nodes/%s/shared/sharedResource.json.gz" % node, slpk))
        response = HTTPResponse(Sharedressource)
        return response
    except Exception as e:
        print(f"Error occurred: {e}")
        return ""


@router.get(
    '/{slpk}/SceneServer/layers/{layer}/nodes/{node}/attributes/{attribute}/0'
)
@router.get(
    '/{slpk}/SceneServer/layers/{layer}/nodes/{node}/attributes/{attribute}/0/'
)
async def attribute_info(slpk, layer, node, attribute):
    """ Attribute information JSON """
    if slpk not in slpks:  # Get 404 if slpk doesn't exists
        abort(404, "Can't found SLPK: %s" % slpk)
    attr_info = await read("nodes/%s/attributes/%s/0.bin.gz" %
                           (node, attribute), slpk)
    response = StreamingResponse(
        BytesIO(attr_info),
        media_type="application/octet-stream; charset=binary"
    )

    return response
