# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.response import Response

from pyramid.httpexceptions import HTTPFound

from ..db import DBSession
from ..models.product import Product

@view_config(route_name='maps', renderer='kj:templates/maps/map.html')
def maps(request):
    products = Product.get_products_eligible_for_map()
    lang_avg = sum([float(p.mlang) for p in products])/len(products)
    long_avg = sum([float(p.mlong) for p in products])/len(products)
    
    return {
        'products': products,
        'lang_avg': lang_avg,
        'long_avg': long_avg
    }
