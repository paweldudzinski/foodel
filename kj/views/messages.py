# -*- coding: utf-8 -*-
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound

from ..lib.helpers import smart_truncate

from ..db import DBSession
from ..models.product import Product
from ..models.thread import Thread


@view_config(route_name='my_threads', permission='user')
def my_threads(request):
    return HTTPFound(location=request.route_path('inbox'))


@view_config(
    route_name='inbox',
    renderer='kj:templates/front/my_messages.html',
    permission='user')
def inbox(request):
    threads_i_sent = request.user.get_active_sender_threads()
    threads_i_get = request.user.get_active_recipient_threads()
    get_unread = 0
    send_unread = 0
    for t in threads_i_get:
        get_unread += len(t.get_unread_messages(request.user))
    for t in threads_i_sent:
        send_unread += len(t.get_unread_messages(request.user))
    return {
        'threads_i_sent': threads_i_sent,
        'threads_i_get': threads_i_get,
        'all_threads': threads_i_get,
        'type': 'INBOX',
        'title': u'Wiadomości wysłane do mnie',
        'get_unread': get_unread,
        'send_unread': send_unread
    }


@view_config(
    route_name='outbox',
    renderer='kj:templates/front/my_messages.html',
    permission='user')
def outbox(request):
    threads_i_sent = request.user.get_active_sender_threads()
    threads_i_get = request.user.get_active_recipient_threads()
    get_unread = 0
    send_unread = 0
    for t in threads_i_get:
        get_unread += len(t.get_unread_messages(request.user))
    for t in threads_i_sent:
        send_unread += len(t.get_unread_messages(request.user))
    return {
        'threads_i_sent': threads_i_sent,
        'threads_i_get': threads_i_get,
        'all_threads': threads_i_sent,
        'type': 'OUTBOX',
        'title': u'Wiadomości wysłane przeze mnie',
        'get_unread': get_unread,
        'send_unread': send_unread
    }


@view_config(
    route_name='archive',
    renderer='kj:templates/front/my_messages.html',
    permission='user')
def archive(request):
    threads_i_sent = request.user.get_archived_sender_threads()
    threads_i_get = request.user.get_archived_recipient_threads()
    get_unread = 0
    send_unread = 0
    return {
        'threads_i_sent': threads_i_sent,
        'threads_i_get': threads_i_get,
        'all_threads': threads_i_sent + threads_i_get,
        'type': 'ARCHIVED',
        'title': u'Wiadomości wysłane przeze mnie',
        'get_unread': get_unread,
        'send_unread': send_unread
    }


@view_config(
    route_name='show_thread_messages',
    renderer='kj:templates/front/message.html',
    permission='user')
def show_thread_messages(request):
    thread_id = request.matchdict.get('id')
    thread = Thread.get(thread_id)

    if not thread or not request.user.can_see_message(thread_id):
        request.session.flash(u'Taka wiadomość nie istnieje')
        return HTTPFound(location=request.route_path('inbox'))

    if thread.recipient != request.user:
        participant = thread.recipient
    else:
        participant = thread.sender

    return {
        'thread': thread,
        'participant': participant,
        'products': participant.get_products_for_message(),
        'title': u"""
            <a class="top-shelf" href="%s">Wiadomości</a> &raquo; %s
        """ % (
            request.route_path('my_threads'),
            smart_truncate(thread.product.name, 65))
    }


@view_config(route_name='send_message',  permission='user')
def send_message(request):
    product_id = request.matchdict.get('product_id')
    product = Product.get(product_id)

    recipient_id = request.matchdict.get('user_id')
    sender_id = request.user.id

    msg = request.params.get('msg')

    if not msg:
        request.session.flash(u'Ej no nie można wysyłać pustej wiadomości...')
        return HTTPFound(location=request.referrer)

    if int(recipient_id) == int(sender_id):
        request.session.flash(u'Ej no nie można wysyłać samemu sobie...')
        return HTTPFound(location=request.referrer)

    existing_thread = Thread.find_by_sender_and_recipient_and_product(
        sender_id, recipient_id, product_id)
    if existing_thread:
        thread = existing_thread
    else:
        thread = Thread()
        thread.from_us_id = sender_id
        thread.to_us_id = recipient_id
        thread.product_id = product_id
        DBSession.add(thread)
        DBSession.flush()

    thread.add_message(sender_id, recipient_id, msg)

    request.session.flash(u'Wiadomość wysłana do %s!' % (product.owner_name()))
    if len(thread.messages) > 1:
        return HTTPFound(location=request.route_path(
            'show_thread_messages',
            id=thread.id,
            _anchor='last_or_new'))
    else:
        return HTTPFound(location=request.referrer)


@view_config(route_name='reply',  permission='user')
def reply(request):
    thread_id = request.matchdict.get('id')
    message = request.params.get('reply')

    if not message:
        request.session.flash(u'Ej no nie można wysyłać pustej wiadomości...')
        return HTTPFound(
            location=request.route_path(
                'show_thread_messages',
                id=thread_id,
                _anchor='last_or_new'))

    thread = Thread.get(thread_id)
    recipient_id = thread.sender.id if thread.sender.id != request.user.id else thread.recipient.id
    thread.add_message(request.user.id, recipient_id, message)

    request.session.flash(u'Wiadomość wysłana!')
    return HTTPFound(location=request.route_path(
        'show_thread_messages', id=thread.id, _anchor='last_or_new'))


@view_config(route_name='archive_message',  permission='user')
def archive_message(request):
    thread_id = request.matchdict.get('id')
    thread = Thread.get(thread_id)

    if not thread or not request.user.can_see_message(thread_id):
        request.session.flash(u'Taka wiadomość nie istnieje')
        return HTTPFound(location=request.route_path('inbox'))
    thread.archive(request.user)
    request.session.flash(u'Wiadomość zarchwizowana!')
    return HTTPFound(location=request.route_path('archive'))
