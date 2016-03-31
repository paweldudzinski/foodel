# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..lib.helpers import chunk
from ..lib.geo import geo
from ..lib.validators import ZipCodeValidator

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
    specyfic = request.params.get('specyfic')
    if keyword and ZipCodeValidator.validate(keyword):
        request.session['search'] = keyword
        keyword = keyword.strip()
    elif keyword:
        request.session.flash(u'Tylko prawidłowy kod pocztowy zadziała...')
        if request.session.get('search'):
            del request.session['search']
        return HTTPFound(location = request.referer)
    else:
        keyword = request.session.get('search')

    if specyfic:
        products = Product.get_all_by_keyword(specyfic)
    else:
        products = Product.get_all()
    products = geo.filter_products(products, keyword, specyfic)
    return {
        'products': chunk(products, request),
        'title': u'Najbliżej Ciebie',
        'keyword': keyword,
        'specyfic': specyfic
    }
