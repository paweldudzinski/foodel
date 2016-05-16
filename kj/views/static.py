# -*- coding: utf-8 -*-
from pyramid.view import view_config


@view_config(
    route_name='terms_and_conditions',
    renderer='kj:templates/static/terms_and_conditions.html')
def terms_and_conditions(request):
    return {
        'title': u'Regulamin korzystania z serwisu internetowego Foodel.pl'
    }
