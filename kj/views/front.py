# -*- coding: utf-8 -*-
from pyramid.view import view_config

from ..lib.helpers import chunk
from ..lib.geo import geo

from ..models.product import Product


@view_config(
    route_name='show_product',
    renderer='kj:templates/front/my_product_for_sale.html')
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


@view_config(route_name='search', renderer='kj:templates/front/show_sale.html')
def search(request):
    keyword = request.params.get('keyword')
    request.session['search'] = keyword
    keyword = keyword.strip()
    products = Product.get_all()
    products = geo.filter_products(products, keyword)
    return {
        'products': chunk(products, request),
        'title': u'Najbliżej Ciebie',
        'keyword': keyword
    }
