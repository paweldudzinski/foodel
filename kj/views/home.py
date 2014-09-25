# -*- coding: utf-8 -*-
import json
import urllib
import cStringIO
import os
import Image
import unicodedata

from hashlib import md5

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
from kj.lib.helpers import make_sef_url, chunk

from ..db import DBSession
from ..models.user import User
from ..models.product import Product
from ..models.category import Category
from ..models.photo import Photo
from ..models.comment import Comment
from ..models.event import Event
from ..lib.validators import NewUserValidator
    
def __get_coupled_categories_for_mosaic(category, where_statement='', mosaic_keys=[]):
    coupled_c = []
    for cat in category.children:
        if cat.coupled:
            for cid in cat.coupled:
                if cid not in mosaic_keys:
                    coupled_c.append(Category.get(cid))
    
    values = []
    for cat in list(set(coupled_c)):
        data = cat.get_current_with_product_ids(where_statement=where_statement)
        if data:
            values.append(data)

    return values
    
@view_config(route_name='home', renderer='kj:templates/index.html')
def home(request):
    mosaic = Category.get_main_with_product_ids(where_statement='AND cat.id != 16')
    mains = Category.get_main_with_product_ids(where_statement='AND cat.id = 16')
    return {
        'mosaic': mosaic,
        'mains' : mains,
        'title': u'Najnowsze, najświeższe, najfajniejsze',
        'main': True
    }
    
@view_config(route_name='home_buy', renderer='kj:templates/index.html')
def home_buy(request):
    mosaic = Category.get_main_with_product_ids(where_statement="AND prod.kind='S'")
    return {
        'mosaic': mosaic,
        'title': u'Do sprzedania',
        'main': True,
        'routing': 'home_buy_show_subcategories'
    }
    
@view_config(route_name='home_change', renderer='kj:templates/index.html')
def home_change(request):
    mosaic = Category.get_main_with_product_ids(where_statement="AND prod.kind='X'")
    return {
        'mosaic': mosaic,
        'title': u'Do wymiany',
        'main': True,
        'routing': 'home_exchange_show_subcategories'
    }

@view_config(route_name='home_show_subcategories', renderer='kj:templates/index.html')
def home_show_subcategories(request):
    category = Category.get(request.matchdict.get('id'))
    mosaic = category.get_subs_product_ids()
    coupled = __get_coupled_categories_for_mosaic(category, mosaic_keys = mosaic.keys())
    return {
        'mosaic' : mosaic,
        'coupled' : coupled,
        'title': category.name,
        'main': False
    }
    
@view_config(route_name='home_buy_show_subcategories', renderer='kj:templates/index.html')    
def home_buy_show_subcategories(request):
    category = Category.get(request.matchdict.get('id'))
    mosaic = category.get_subs_product_ids(where_statement="AND prod.kind='S'")
    coupled = __get_coupled_categories_for_mosaic(category, where_statement="AND prod.kind='S'", mosaic_keys = mosaic.keys())

    return {
        'mosaic' : mosaic,
        'coupled' : coupled,
        'title': category.name,
        'main': False,
        'routing': 'home_show_buy_products'
    }

@view_config(route_name='home_exchange_show_subcategories', renderer='kj:templates/index.html')    
def home_exchange_show_subcategories(request):
    category = Category.get(request.matchdict.get('id'))
    mosaic = category.get_subs_product_ids(where_statement="AND prod.kind='X'")
    coupled = __get_coupled_categories_for_mosaic(category, where_statement="AND prod.kind='X'", mosaic_keys = mosaic.keys())
    return {
        'mosaic' : mosaic,
        'coupled' : coupled,
        'title': category.name,
        'main': False,
        'routing': 'home_show_exchange_products'
    }
    
@view_config(route_name='home_show_products', renderer='kj:templates/products.html')    
def home_show_products(request):
    category = Category.get(request.matchdict.get('id'))
    q = Product.get_by_subcategory(category.id)
    products = chunk(q, request)
    return {
        'products': products,
        'title': u'<a class="top-shelf" href="%s">%s</a> &raquo; %s' % (request.route_path('home_show_subcategories', id=category.parent.id, sef=make_sef_url(category.parent.name)), category.parent.name, category.name)
    }

@view_config(route_name='home_show_buy_products', renderer='kj:templates/products.html')  
def home_show_buy_products(request):
    category = Category.get(request.matchdict.get('id'))
    q = Product.get_by_subcategory(category.id, kind='S')
    products = chunk(q, request)
    return {
        'products': products,
        'title': u'<a class="top-shelf" href="%s">%s</a> &raquo; %s' % (request.route_path('home_buy_show_subcategories', id=category.parent.id, sef=make_sef_url(category.parent.name)), category.parent.name, category.name)
    }

@view_config(route_name='home_show_exchange_products', renderer='kj:templates/products.html')  
def home_show_exchange_products(request):
    category = Category.get(request.matchdict.get('id'))
    q = Product.get_by_subcategory(category.id, kind='X')
    products = chunk(q, request)
    return {
        'products': products,
        'title': u'<a class="top-shelf" href="%s">%s</a> &raquo; %s' % (request.route_path('home_exchange_show_subcategories', id=category.parent.id, sef=make_sef_url(category.parent.name)), category.parent.name, category.name)
    }

@view_config(route_name='save_comment')  
def save_comment(request):
    product = Product.get(request.matchdict.get('id'))
    comment = request.params.get('comment')
    if not product or not request.user:
        abort(404)
    if not comment:
        request.session.flash(u'Komentarz nie może być pusty...')
        return HTTPFound(location = request.referer)
        
    Comment.add(product, comment, request.user)
    request.session.flash(u'Komentarz dodany!')
    return HTTPFound(location = "%s#comments"%(request.referer))

@view_config(route_name='home_events', renderer='kj:templates/events.html')
def home_events(request):
    return {
        'title': u'Wydarzenia',
        'events': Event.get_all_active()
    }

@view_config(route_name='home_event', renderer='kj:templates/front/show_event.html')    
def home_event(request):
    event = Event.get(request.matchdict.get('id'))
    
    if not event:
        request.session.flash(u'Błąd w formularzu, coś poszło nie tak...')
        HTTPFound(location = request.route_url('register'))
    
    return {
        'title': u'Wydarzenia &raquo; %s' % (event.title),
        'event': event
    }
    

@forbidden_view_config(renderer='pj:templates/index.html')
def forbidden(request):
    request.session.flash(u'Zaloguj się żeby zobaczyć tę stronę')
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers)
    
@view_config(route_name='register', renderer='kj:templates/register.html')
def register(request):
    return {
        'title' : u'Rejestracja'
    }
    
@view_config(route_name='save_user')
def save_user(request):
    validated = NewUserValidator.validate(request.params.mixed())
    
    existing = User.get_by_email(request.params.get('email'))
    if existing:
        return HTTPFound(location = request.route_url('registered_already'))
    
    if validated :
        User.save_new(request.params.mixed())
    else:
        request.session.flash(u'Błąd w formularzu, coś poszło nie tak...')
        HTTPFound(location = request.route_url('register'))
        
    return HTTPFound(location = request.route_url('register_thanks'))

@view_config(route_name='register_thanks', renderer='kj:templates/register_confirm.html')
def register_thanks(request):
    return {
        'title' : u'Rejestracja'
    }
    
@view_config(route_name='register_email_thanks', renderer='kj:templates/register_email_confirm.html')
def register_email_thanks(request):
    return {}

@view_config(route_name='register_email_failed', renderer='kj:templates/register_email_confirm_failed.html')
def register_email_failed(request):
    return {
        'title' : u'Rejestracja'
    }

@view_config(route_name='registered_already', renderer='kj:templates/registered_already.html')    
def registered_already(request):
    return {
        'title' : u'Rejestracja'
    }

@view_config(route_name='register_confirm')
def register_confirm(request):
    user_id = request.matchdict.get('id')
    md5 = request.matchdict.get('md5')
    user = User.get_by_id_and_md5(user_id, md5)
    if user:
        user.confirm()
        return HTTPFound(location = request.route_url('register_email_thanks'))
    else:
        return HTTPFound(location = request.route_url('register_email_failed'))

@view_config(route_name='login')
def login(request):
    login_url = request.route_url('login')
    referrer = request.referer
    if referrer == login_url:
        referrer = '/' 
    came_from = request.params.get('came_from', referrer)
    
    if 'form.submitted' in request.params:
        login = request.params.get('email')
        password = request.params.get('password')
    
        user = User.login(login, password)
        if user:
            headers = remember(request, user.id)
            return HTTPFound(location = came_from,
                             headers = headers)
    
    request.session.flash(u'Błąd logowaaaniaaaa!')
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers)

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                      headers=headers)

@view_config(renderer='json', route_name='fb_login') 
def fb_login(request):
    user = User.get_by_email(request.params.get('response[email]'))
    if not user:
        data = {}
        name = data['name'] = request.params.get('response[name]', 'Nieznane z Facebooka')
        email = data['email'] = request.params.get('response[email]', 'unknown@facebook.com')
        user = User.save_new(data, generate_password=True)
        
        URL = 'http://graph.facebook.com/%s/picture?type=large' % (request.params.get('response[id]'))
        file_content = urllib.urlopen(URL).read()
        if file_content and user:
            filename, ext = request.params.get('response[username]') or request.params.get('response[last_name]') or 'unknown', '.jpg'
            filename = unicodedata.normalize('NFD', filename).encode('ascii', 'ignore')
            md5_ = md5(str(file_content)).hexdigest()
            new_filename = md5_ + '_' + filename.lower() + ext.lower()
            if not os.path.exists(Photo.BASE_STORAGE_PATH + new_filename[0]):
                    os.makedirs(Photo.BASE_STORAGE_PATH + new_filename[0])
                    
            new_filename_with_path = Photo.BASE_STORAGE_PATH + new_filename[0] + '/' + new_filename
            
            Photo.save_original(new_filename_with_path, file_content)
            
            img = Image.open(new_filename_with_path)
            if img.mode != "RBG":
                img = img.convert("RGB")
            avatar_image = Photo.resize(img, Photo.AVATAR_THUMBNAIL, new_filename, 'avatar_')
            tiny_image = Photo.resize(img, Photo.TINY_THUMBNAIL, new_filename, 'tiny_')
            small_image = Photo.resize(img, Photo.SMALL_THUMBNAIL, new_filename, 'small_')
            big_image = Photo.resize(img, Photo.BIG_THUMBNAIL, new_filename, 'big_')
            maxi_image = Photo.resize(img, Photo.MAXI_THUMBNAIL, new_filename, 'maxi_')

            user.save_avatar(new_filename_with_path)
            
    request_url = request.route_url('login', _query={'form.submitted':'1', 'email':user.email, 'password':user.password})   
    return json.dumps({"request_url" : "%s"%(request_url)})








