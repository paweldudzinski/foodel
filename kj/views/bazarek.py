# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import exception_response

from ..lib.helpers import make_sef_url, chunk
from ..models.user import User


@view_config(
    route_name='profile_link',
    renderer='kj:templates/profile/profile.html')
def bazarek(request):
    user = User.get(request.matchdict.get('id', 0))
    sef = request.matchdict.get('sef', 'secret_sef')
    user_sef = make_sef_url(user and user.user_name() or 'secret_user_name')

    if not user or sef != user_sef:
        return exception_response(404)

    return {
        'products': chunk(user.get_all_products(), request),
        'title': "Bazarek: %s" % (user.user_name()),
        'main': True,
        'user': user
    }
