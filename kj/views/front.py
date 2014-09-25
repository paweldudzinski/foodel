# -*- coding: utf-8 -*-
from pyramid.response import Response
from pyramid.view import (
    view_config,
    forbidden_view_config
    )

from pyramid.security import (
    remember,
    forget,
    )

from hashlib import md5

from pyramid.httpexceptions import HTTPFound

from ..lib.helpers import make_sef_url, chunk

from ..db import DBSession
from ..models.user import User
from ..models.product import Product

@view_config(route_name='show_product', renderer='kj:templates/front/my_product_for_sale.html')
def show_product(request):
    product_id = request.matchdict.get('id')
    product = Product.get(product_id)
    exchange_offers = product.kind == Product.KIND_EXCHANGE and product.exchange_offers or []
    return {
        'exchange_offers': [Product.get(x) for x in exchange_offers],
        'product': product,
        'title': product.html_breadcrumb(request),
        'logged_user_products': product.kind == product.BARGAIN_EXCHANGE and request.user and request.user.get_all_products() or []
    }

@view_config(route_name='show_sale', renderer='kj:templates/front/show_sale.html')
def show_sale(request):
    products = Product.get_all_for_sale()
    return {
        'products' : []
    }

@view_config(route_name='search', renderer='kj:templates/front/show_sale.html')
def search(request):
    keyword = request.params.get('keyword');
    keyword = keyword.strip()
    products = Product.get_all_by_keyword(keyword)
    return {
        'products': chunk(products, request),
        'title': u'Poszukiwania dla słowa: %s' % (keyword),
        'keyword': keyword
    }
