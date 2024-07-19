from .index import *
from .map import *
from .p404 import *

ROUTES = {
    "/": page_index,
    "/map": page_map,
    "/404": page_404
}