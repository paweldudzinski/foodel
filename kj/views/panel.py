# -*- coding: utf-8 -*-
import os
import Image
import unicodedata
import datetime

from pyramid.response import Response
from pyramid.renderers import render

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

from ..db import DBSession
from ..models.user import User
from ..models.photo import Photo
from ..models.product import Product
from ..models.category import Category
from ..models.specifics import Specifics
from ..models.location import Location
from ..models.lead import Lead
from ..models.event import Event
from ..lib.validators import NewUserValidator

@view_config(route_name='pa_home', permission='user')    
def pa_home(request):
    return HTTPFound(location=request.route_url('my_product_for_sale'))

@view_config(route_name='pa_edit_me', renderer='kj:templates/panel/index.html', permission='user')
def pa_edit_me(request):
    return {}

@view_config(route_name='save_edited_user', permission='user')
def save_edited_user(request):
    validated = NewUserValidator.validate(request.params.mixed())
    user = User.get_by_email(request.params.get('email'))
    
    if validated and user:
        user.save_edited(request.params.mixed())
        avatar = request.params.get('avatar')
        if len(str(avatar)):
            if type(avatar) is type(''): 
                request.session.flash(u'Błąd pliku awatara.')
                return HTTPFound(location=request.route_url('pa_home'))
                
            file_content = avatar.file.read()
            if len(file_content) == 0: 
                request.session.flash(u'Błąd pliku awatara.')
                return HTTPFound(location=request.route_url('pa_home'))
                
            filename, ext = os.path.splitext(avatar.filename)
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
                
        request.session.flash(u'Zapisałem!')
    else:
        request.session.flash(u'Błąd w formularzu, coś poszło nie tak...')
        
    return HTTPFound(location = request.route_url('pa_home')) 

@view_config(route_name='my_product_for_sale', renderer='kj:templates/panel/my_sale.html', permission='user')
def my_product_for_sale(request):
    products = request.user.get_all_products_for_sale()
    return {
        'products' : products,
        'type' : Product.KIND_SELL
    }

@view_config(route_name='my_product_for_exchange', renderer='kj:templates/panel/my_sale.html', permission='user')
def my_product_for_exchange(request):
    products = request.user.get_all_products_for_exchange()
    return {
        'products' : products,
        'type' : Product.KIND_EXCHANGE
    }

@view_config(route_name='add_exchange', renderer='kj:templates/panel/add_sale.html', permission='user')
def add_exchange(request):
    av = []
    for a in Product.AVAILABILITIES_ORDER:
        av.append((a, Product.AVAILABILITIES[a]))
        
    so = []
    for a in Product.SHIPPINGS_ORDER:
        so.append((a, Product.SHIPPINGS[a]))
        
    ev = []
    for a in Product.END_DATES_ORDER:
        ev.append((a, Product.END_DATES[a]))
        
    qm = []
    for a in Product.QUANTITY_MEASURES:
        qm.append((a, Product.QUANTITY_MEASURES[a]))
        
    woj_loc = []
    for a in Location.get_main():
        woj_loc.append((a.id, a.name))
        
    categories = []
    for c in Product.get_all_categories_for_products():
        categories.append((c.id, c.name))
        
    specifics = Specifics.all()
        
    return {
        'bargain_values' : tuple(Product.BARGAINS.iteritems()),
        'availabilility_values' : av,
        'shipping_values' : so,
        'end_date_values' : ev,
        'quantity_measures' : qm,
        'categories' : categories,
        'specifics' : specifics,
        'wojewodztwa' : woj_loc,
        'type' : 'EXCHANGE'
    }

@view_config(route_name='add_sale', renderer='kj:templates/panel/add_sale.html', permission='user')
def add_sale(request):
    av = []
    for a in Product.AVAILABILITIES_ORDER:
        av.append((a, Product.AVAILABILITIES[a]))
        
    so = []
    for a in Product.SHIPPINGS_ORDER:
        so.append((a, Product.SHIPPINGS[a]))
        
    ev = []
    for a in Product.END_DATES_ORDER:
        ev.append((a, Product.END_DATES[a]))
        
    qm = []
    for a in Product.QUANTITY_MEASURES:
        qm.append((a, Product.QUANTITY_MEASURES[a]))
        
    woj_loc = []
    for a in Location.get_main():
        woj_loc.append((a.id, a.name))
        
    categories = []
    for c in Product.get_all_categories_for_products():
        categories.append((c.id, c.name))
        
    specifics = Specifics.all()
        
    return {
        'bargain_values' : tuple(Product.BARGAINS.iteritems()),
        'availabilility_values' : av,
        'shipping_values' : so,
        'end_date_values' : ev,
        'categories' : categories,
        'quantity_measures' : qm,
        'specifics' : specifics,
        'wojewodztwa' : woj_loc,
        'type' : 'SALE'
    }

@view_config(route_name='save_product_for_sale', permission='user')
def save_product_for_sale(request):
    product = Product.save_product_for_sale(request.params.mixed(), request.user.id)
    main_photo = request.params.get('foto_main','')
    foto_1 = request.params.get('foto_1','')
    foto_2 = request.params.get('foto_2','')
    
    if len(str(main_photo)):
        photo = product.save_product_photo(main_photo, main=True)
        if not photo:
            raise Exception("Not Implemented")
            
    if len(str(foto_1)):
        photo = product.save_product_photo(foto_1, main=False)
        if not photo:
            raise Exception("Not Implemented")
    
    if len(str(foto_2)):
        photo = product.save_product_photo(foto_2, main=False)
        if not photo:
            raise Exception("Not Implemented")
    
    product.save_geolocalisation()
    request.session.flash(u'Zapisałem!')
    return HTTPFound(location = request.route_url('add_sale'))

@view_config(route_name='save_edited_product_for_sale', permission='user')
def save_edited_product_for_sale(request):
    request.session.flash(u'Zapisałem!')
    product_id = request.matchdict.get('id')
    main_photo = request.params.get('foto_main','')
    foto_1 = request.params.get('foto_1','')
    foto_2 = request.params.get('foto_2','')
    
    product = Product.get(product_id)
    product.save_edited_product_for_sale(request.params.mixed())
    
    if len(str(main_photo)):
        photo = product.save_product_photo(main_photo, main=True)
        if not photo:
            raise Exception("Not Implemented")
            
    if len(str(foto_1)):
        photo = product.save_product_photo(foto_1, main=False)
        if not photo:
            raise Exception("Not Implemented")
    
    if len(str(foto_2)):
        photo = product.save_product_photo(foto_2, main=False)
        if not photo:
            raise Exception("Not Implemented")
    
    product.save_geolocalisation()
    return HTTPFound(location = request.route_url('edit_product_for_sale', id=product.id, user=product.user.id))

@view_config(route_name='delete_product', permission='user')
def delete_product(request):
    product_id = request.matchdict.get('id')
    user_id = request.matchdict.get('user')

    product = Product.get(product_id)
    kind = product and product.kind
    
    if int(request.user.id) == int(user_id) and product_id:
        Product.delete_one(product_id)
        request.session.flash(u'Usunąłem!')
    else:
        request.session.flash(u'Nie znaleziono produktu!')
    
    if kind == Product.KIND_SELL:
        return HTTPFound(location = request.route_url('my_product_for_sale'))
    else:
        return HTTPFound(location = request.route_url('my_product_for_exchange'))
        
@view_config(route_name='delete_photo', permission='user')
def delete_photo(request):
    photo_id = request.matchdict.get('id')
    photo = Photo.get_by_id(photo_id)
    Photo.delete_one(photo)
    return HTTPFound(location = request.referer)
    
@view_config(route_name='edit_product_for_sale', renderer='kj:templates/panel/edit_sale.html', permission='user')
def edit_product_for_sale(request):
    product_id = request.matchdict.get('id')
    user_id = request.matchdict.get('user')
    
    if int(request.user.id) != int(user_id) and product_id:
        request.session.flash(u'Nie znaleziono produktu!')
        return HTTPFound(location = request.route_url('my_product_for_sale'))
        
    av = []
    for a in Product.AVAILABILITIES_ORDER:
        av.append((a, Product.AVAILABILITIES[a]))
        
    so = []
    for a in Product.SHIPPINGS_ORDER:
        so.append((a, Product.SHIPPINGS[a]))
        
    ev = []
    for a in Product.END_DATES_ORDER:
        ev.append((a, Product.END_DATES[a]))
        
    
        
    product = Product.get(product_id)
        
    categories = []
    for c in Product.get_all_categories_for_products():
        categories.append((c.id, c.name))
        
    subcategories = []
    subcategories2 = []
    for c in product.category.children:
        subcategories.append((c.id, c.name))
        if product.subcat_id != c.id:
            subcategories2.append((c.id, c.name))
            
    woj_loc = []
    for a in Location.get_main():
        woj_loc.append((a.id, a.name))
    cit_loc = []
    if product.location:
        for c in product.location.wojewodztwo.cities:
            cit_loc.append((c.id, c.name))
        
    return {
        'product' : product,
        'bargain_values' : tuple(Product.BARGAINS.iteritems()),
        'availabilility_values' : av,
        'shipping_values' : so,
        'end_date_values' : ev,
        'categories' : categories,
        'subcategories' : subcategories,
        'subcategories2' : subcategories2,
        'wojewodztwa' : woj_loc,
        'cities' : cit_loc
    }
        
@view_config(renderer="json", route_name="load_subcategories")
def load_subcategories(request):
    category = Category.get(request.matchdict.get('id'))
    categories = []
    for c in category.children:
        categories.append((c.id, c.name))
    
    renderer_dict = {
        'categories' : categories
    } 
    select = render('kj:templates/panel/subcategories.html', renderer_dict, request)
    return select
    
@view_config(renderer="json", route_name="load_cities")
def load_cities(request):
    wojewodztwo = Location.get(request.matchdict.get('id'))
    cities = []
    for c in wojewodztwo.cities:
        cities.append((c.id, c.name))
    
    renderer_dict = {
        'cities' : cities
    } 
    select = render('kj:templates/panel/cities.html', renderer_dict, request)
    return select
    
@view_config(renderer="json", route_name="load_subcategories2")
def load_subcategories2(request):
    category = Category.get(request.matchdict.get('id'))
    categories = []
    for c in category.parent.children:
        if c.id != int(request.matchdict.get('id')):
            categories.append((c.id, c.name))
    
    renderer_dict = {
        'categories' : categories
    } 
    select = render('kj:templates/panel/subcategories2.html', renderer_dict, request)
    return select

@view_config(renderer="json", route_name="load_couple")
def load_couple(request):
    category = Category.get(request.matchdict.get('id'))
    part = ('<br />').join(["&bull; %s &rarr; %s"%(cat.parent.name, cat.name) for cat in category.coupled_categories])
    part += '<br />'
    part += '<a style="margin-top:10px;" class="btn btn-primary btn-medium" href="/edytuj-sparowane/%s">Edytuj</a>' % (category.id)
    return part

@view_config(route_name='category_coupling', renderer='kj:templates/panel/category_coupling.html', permission='user')
def category_coupling(request):
    return {
        'cat_not_coupled': Category.get_not_coupled(),
        'cat_coupled': Category.get_coupled(),
        'cat_for_coupling': Category.get_for_coupling()
    }
    
@view_config(route_name='save_couple', permission='user')
def save_couple(request):
    base_cat_id = request.params.get('base_cat')
    cat1 = request.params.get('cat1')
    cat2 = request.params.get('cat2')
    cat3 = request.params.get('cat3')
    
    if not base_cat_id or not any([cat1, cat2, cat2]):
        request.session.flash(u'Trzeba wybrać kategorię baząwą i te sprzężone...')
        return HTTPFound(location = request.referer)
    
    base_cat = Category.get(base_cat_id)
    
    cat_list = list(set([cat1, cat2, cat3]))
    eligible_cats = []
    for cat in cat_list:
        if cat:
            eligible_cats.append(int(cat))
    
    base_cat.coupled = eligible_cats
    DBSession.flush()
    
    request.session.flash(u'Zapisane!')
    return HTTPFound(location = request.referer)

@view_config(route_name='edit_couple', renderer='kj:templates/panel/edit_couple.html', permission='user')
def edit_couple(request):
    category = Category.get(request.matchdict.get('id'))
    return {
        'category' : category,
        'cat_for_coupling': Category.get_for_coupling()
    }
    
@view_config(route_name='save_edited_couple', permission='user')
def save_edited_couple(request):
    base_cat = Category.get(request.matchdict.get('id'))
    cat1 = request.params.get('cat1')
    cat2 = request.params.get('cat2')
    cat3 = request.params.get('cat3')
    
    if not base_cat or not any([cat1, cat2, cat2]):
        request.session.flash(u'Trzeba wybrać te sprzężone...')
        return HTTPFound(location = request.referer)
        
    cat_list = list(set([cat1, cat2, cat3]))
    
    if str(base_cat.id) in cat_list:
        request.session.flash(u'Nie można sprzężyć samego siebie...')
        return HTTPFound(location = request.referer)
    
    eligible_cats = []
    for cat in cat_list:
        if cat:
            eligible_cats.append(int(cat))
    
    base_cat.coupled = eligible_cats
    DBSession.flush()
    
    request.session.flash(u'Zapisane!')
    return HTTPFound(location=request.route_url('category_coupling'))

@view_config(route_name='leads', renderer='kj:templates/panel/edit_leads.html', permission='user')
def leads(request):
    return {
        'leads': Lead.all(),
        'categories': list(Lead.LC_NAMES.items()),
        'chosen_lead': None
    }
    
@view_config(route_name='edit_lead', renderer='kj:templates/panel/edit_leads.html', permission='user')
def edit_lead(request):
    return {
        'chosen_lead': Lead.get(request.matchdict.get('id')),
        'categories': list(Lead.LC_NAMES.items())
    }
    
@view_config(route_name='save_lead', permission='user')
def save_lead(request):
    name = request.params.get('name')
    email = request.params.get('email')
    phone = request.params.get('phone')
    description = request.params.get('description')
    category = request.params.get('category')
    Lead.save(name, email, phone, description, category)
    request.session.flash(u'Zapisane!')
    return HTTPFound(location=request.route_url('leads'))

@view_config(route_name='save_edited_lead', permission='user')
def save_edited_lead(request):
    lead = Lead.get(request.matchdict.get('id'))
    name = request.params.get('name')
    email = request.params.get('email')
    phone = request.params.get('phone')
    description = request.params.get('description')
    category = request.params.get('category')
    lead.update(name, email, phone, description, category)
    request.session.flash(u'Zapisane!')
    return HTTPFound(location=request.route_url('leads'))

@view_config(route_name='delete_lead', permission='user')
def delete_lead(request):
    lead_id = request.matchdict.get('id')
    Lead.delete(lead_id)
    request.session.flash(u'Usunięty!')
    return HTTPFound(location=request.route_url('leads'))

@view_config(route_name='my_events', renderer='kj:templates/panel/my_events.html', permission='user')
def my_events(request):
    return {
        'events': request.user.get_active_events(),
        'past_events': request.user.get_unactive_events()
    }

@view_config(route_name='add_event', renderer='kj:templates/panel/edit_events.html', permission='user')    
def add_event(request):
    woj_loc = []
    for a in Location.get_main():
        woj_loc.append((a.id, a.name))

    return {
        'new': True,
        'event': None,
        'wojewodztwa': woj_loc
    }
    
@view_config(route_name='edit_event', renderer='kj:templates/panel/edit_events.html', permission='user')    
def edit_event(request):
    event = Event.get(request.matchdict.get('id'))
    if not event or not event.is_mine(request.user):
        request.session.flash(u'Nie ma takiego wydarzenia')
        return HTTPFound(location=request.route_url('my_events'))
        
    woj_loc = []
    for a in Location.get_main():
        woj_loc.append((a.id, a.name))
    cit_loc = []
    if event.location:
        for c in event.location.wojewodztwo.cities:
            cit_loc.append((c.id, c.name))
        
    return {
        'new': False,
        'event': event,
        'wojewodztwa' : woj_loc,
        'cities' : cit_loc
    }
    
@view_config(route_name='save_event', permission='user')
def save_event(request):
    title = request.params.get('title')
    description = request.params.get('description')
    date_from = request.params.get('date_from')
    date_to = request.params.get('date_to')
    foto = request.params.get('foto')
    city = request.params.get('city')
    facebook_url = request.params.get('facebook_url')
    start_hour = request.params.get('start_hour')
    start_minute = request.params.get('start_minute')
    street = request.params.get('street')

    event = Event.create(
        request.user.id,
        title,
        description,
        date_from,
        date_to,
        city,
        street,
        start_hour,
        start_minute,
        facebook_url
    )
    
    if len(str(foto)):
        photo = event.save_event_photo(event.id, foto)
        if not photo:
            raise Exception("Not Implemented")

    event.save_geolocalisation()
    request.session.flash(u'Wydarzenie zostało dodane!')
    return HTTPFound(location=request.route_url('my_events'))

@view_config(route_name='save_edited_event', permission='user')
def save_edited_event(request):
    event = Event.get(request.matchdict.get('id'))
    if not event or not event.is_mine(request.user):
        request.session.flash(u'Nie ma takiego wydarzenia')
        return HTTPFound(location = request.referer)
    
    title = request.params.get('title')
    description = request.params.get('description')
    date_from = request.params.get('date_from')
    date_to = request.params.get('date_to')
    foto = request.params.get('foto')
    city = request.params.get('city')
    facebook_url = request.params.get('facebook_url')
    start_hour = request.params.get('start_hour')
    start_minute = request.params.get('start_minute')
    street = request.params.get('street')

    event.title = title
    event.description = description
    event.date_from = datetime.datetime.strptime(date_from, '%d-%m-%Y')
    event.date_to = date_to and datetime.datetime.strptime(date_to, '%d-%m-%Y')
    event.loc_id = city
    event.facebook_url = facebook_url
    event.street = street
    event.event_time = '%s:%s' % (start_hour, start_minute)
    
    if city:
        city = Location.get(city)
        if city:
            event.localisation = "%s, %s, Polska" % (city.name, city.wojewodztwo.name.lower())
    
    if len(str(foto)) and foto != None:
        photo = event.save_event_photo(event.id, foto)
        if not photo:
            raise Exception("Not Implemented")
    
    event.save_geolocalisation()
    request.session.flash(u'Wydarzenie zapisane!')
    return HTTPFound(location=request.route_url('my_events'))
    
    
@view_config(route_name='delete_event', permission='user')    
def delete_event(request):
    event = Event.get(request.matchdict.get('id'))
    if not event or not event.is_mine(request.user):
        request.session.flash(u'Nie ma takiego wydarzenia')
        return HTTPFound(location=request.route_url('my_events'))
    
    event.delete()
    request.session.flash(u'Wydarzenie usunięte')
    return HTTPFound(location=request.route_url('my_events'))
    
    
    
    
