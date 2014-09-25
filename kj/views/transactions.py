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
    
from pyramid.httpexceptions import HTTPFound
from ..lib.email_sender import EmailSender

from ..db import DBSession
from ..models.product import Product
from ..models.order import Order

@view_config(route_name='buy')
def buy(request):
    quantity = request.params.get('quantity')
    msg = request.params.get('msg')
    product = Product.get(request.matchdict.get('id'))
    
    seller = product.user
    buyer = request.user
    
    if seller == buyer:
        request.session.flash(u'Ej no nie można wysyłać samemu sobie...')
        return HTTPFound(location=request.referer)
    
    o = Order.new(seller=seller, buyer=buyer, product=product, quantity=quantity, message=msg)
    product.decrease_quantity(quantity)
    o.mark(Order.OS_FINISHED, seller.id)
    o.mark(Order.OS_FINISHED, buyer.id)
    
    EmailSender.send_product_bought_email(buyer, product)
    
    request.session.flash(u'Kupione!')
    return HTTPFound(location=request.route_path('show_thread_messages', id=o.thread.id, _anchor='last_or_new'))

@view_config(route_name='exchange')    
def exchange(request): 
    product = Product.get(request.matchdict.get('id'))
    product_for_exchange = Product.get(request.params.get('product_for_exchange'))
    
    if not product or not product_for_exchange:
        request.session.flash(u'Oj, coś poszło nie tak :(')
        return HTTPFound(location=request.referer)
    
    existing_list = product.exchange_offers or []
    
    if product_for_exchange.id in existing_list:
        request.session.flash(u'Ten produkt już zaoferowałeś do wymiany.')
        return HTTPFound(location=request.referer)
    
    existing_list.append(product_for_exchange.id)
    product.exchange_offers = list(set(existing_list))
    DBSession.flush()            
    request.session.flash(u'Prośba o wymienę została wysłana! Jeżeli druga strona się zgodzi na wymianę, zostaniesz o tym powiadomiony!')
    return HTTPFound(location=request.referer)

def _get_counts_as_dict(count_dict):
    result = {
        Order.OS_NEW: 0,
        Order.OS_FINISHED: 0,
        Order.OS_CANCELLED: 0
    }
    for cd in count_dict:
        result[cd.status] = cd.count
    return result   

@view_config(route_name='my_orders_sold', renderer='kj:templates/panel/my_orders_sold.html', permission='user')
def my_orders_sold(request):
    order_kind = request.matchdict.get('kind', 'nowe')
    if order_kind not in Order.ALLOWED_TYPES:
        order_kind = 'nowe'
    
    filters = _get_filters(request)
    
    sold_counts = request.user.get_sold_all_orders_counts_as_dict(filters)
    orders = request.user.get_sold_orders_by_type(Order.ORDER_TO_URL.get(order_kind), filters)
    return {
        'sold_counts': _get_counts_as_dict(sold_counts),
        'title': order_kind.capitalize(),
        'orders': orders,
        'TIMES_SORTED' : Order.TIMES_SORTED,
        'TIMES' : Order.TIMES,
        'TYPE_SORTED_SORTED' : Order.TYPE_SORTED_SORTED,
        'TYPE_SORTED' : Order.TYPE_SORTED,
        'tfilters' : _get_filters(request)
    }
    
@view_config(route_name='my_orders_bought', renderer='kj:templates/panel/my_orders_bought.html', permission='user')
def my_orders_bought(request):
    order_kind = request.matchdict.get('kind', 'zakonczone')
    if order_kind not in Order.ALLOWED_TYPES:
        order_kind = 'zakonczone'
    
    filters = _get_filters(request)
    
    bought_counts = request.user.get_bought_all_orders_counts_as_dict(filters)
    orders = request.user.get_bought_orders_by_type(Order.ORDER_TO_URL.get(order_kind), filters)
    gradable_orders = request.user.get_orders_to_grade(filters)
    return {
        'bought_counts': _get_counts_as_dict(bought_counts),
        'title': order_kind.capitalize(),
        'orders': orders,
        'gradable_orders' : gradable_orders,
        'TIMES_SORTED' : Order.TIMES_SORTED,
        'TIMES' : Order.TIMES,
        'TYPE_SORTED_SORTED' : Order.TYPE_SORTED_SORTED,
        'TYPE_SORTED' : Order.TYPE_SORTED,
        'tfilters' : filters
    }
    
@view_config(route_name='change_order_state', permission='user')
def change_order_state(request):
    order_id = request.matchdict.get('id')
    new_state = request.params.get('order_new_kind')
    order = Order.get(order_id)
    order.mark(new_state, request.user.id)
    if new_state == Order.OS_CANCELLED:
        order.product.increase_quantity(order.quantity)
    return HTTPFound(location=request.referer)

@view_config(route_name='orders_for_grading', renderer='kj:templates/panel/orders_for_grading.html', permission='user')    
def orders_for_grading(request):
    order_kind = request.matchdict.get('kind', 'nowe')
    if order_kind not in Order.ALLOWED_TYPES:
        order_kind = 'nowe'
    
    filters = _get_filters(request)
        
    bought_counts = request.user.get_bought_all_orders_counts_as_dict(filters)
    orders = request.user.get_bought_orders_by_type(Order.ORDER_TO_URL.get(order_kind), filters)
    gradable_orders = request.user.get_orders_to_grade(filters)
        
    if not gradable_orders:
        return HTTPFound(location=request.route_path('my_orders_bought', kind='nowe'))
    
    return {
        'bought_counts': _get_counts_as_dict(bought_counts),
        'title': order_kind.capitalize(),
        'orders': gradable_orders,
        'gradable_orders' : gradable_orders,
        'gradable_orders' : gradable_orders,
        'TIMES_SORTED' : Order.TIMES_SORTED,
        'TIMES' : Order.TIMES,
        'TYPE_SORTED_SORTED' : Order.TYPE_SORTED_SORTED,
        'TYPE_SORTED' : Order.TYPE_SORTED,
        'tfilters' : filters
    }

@view_config(route_name='ajax_get_order_to_grade', renderer='kj:templates/panel/ajax_get_order_to_grade.html', permission='user')
def ajax_get_order_to_grade(request):
    order_id = request.matchdict.get('id')
    order = Order.get(order_id)
    can_grade_order = order.can_grade_order(request.user.id)
    
    return {
        'can_grade_order': can_grade_order,
        'order': order
    }

@view_config(route_name='save_grade', permission='user')
def save_grade(request):
    order_id = request.matchdict.get('order_id')
    grade = request.matchdict.get('grade')
    
    order = Order.get(order_id)
    
    if not order.can_grade_order(request.user.id) or order.is_graded_by_me(request.user.id, order.product.id):
        request.session.flash(u'Nie masz uprawnień do oceny tego przedmiotu...')
        return HTTPFound(location=request.referer)
    
    order.grade(grade)
    
    request.session.flash(u'Dzięki za wystawienie oceny!')
    return HTTPFound(location=request.referer)
    
@view_config(route_name='transactions_apply_filter', permission='user')
def transactions_apply_filter(request):
    response = request.response
    response.set_cookie('filter_time', request.params.get('time', Order.TIME_WEEK))
    response.set_cookie('filter_type', request.params.get('sort', Order.BY_TIME))
    return HTTPFound(location=request.referer, headers=response.headers)
    
def _get_filters(request):
    return {
        'time': request.cookies.get('filter_time', Order.TIME_WEEK),
        'type': request.cookies.get('filter_type', Order.BY_TIME)
    }
    
    
    
    
    
    
