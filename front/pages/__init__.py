from .index import *
from .map import *
from .p404 import *
from .api import *
from .links import *
from .device_uid import *

ROUTES = {
    "/": page_index,
    "/map": page_map,
    "/404": page_404,
    "/api": page_api,
    "/links": page_links,
    "/device/<>": page_device_uid
}