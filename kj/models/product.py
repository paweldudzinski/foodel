# -*- coding: utf-8 -*-
import os
from PIL import Image
import math
import datetime
import unicodedata

from hashlib import md5
from sqlalchemy.dialects.postgresql import ARRAY as PGArray

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Numeric,
    DateTime,
    and_,
    or_,
    func,
    )

from sqlalchemy.orm import (
    relationship,
    backref,
    )

from ..db import (
    Base,
    KJBase,
    DBSession,
    )

from kj.lib.helpers import make_sef_url

from photo import Photo
from category import Category
from vote import Vote
from specifics import Specifics
from location import Location


class Product(Base, KJBase):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    kind = Column(String(1))
    state = Column(String(1), default='A')
    localisation = Column(String(1000))
    bargain_type = Column(String(1))
    bargain_type_freetext = Column(Text)
    mlang = Column(String(100))
    mlong = Column(String(100))

    price = Column(Numeric(asdecimal=True))
    availability = Column(String(1))
    shipping_method = Column(String(1))
    shipping_method_freetext = Column(Text)
    shipping_price = Column(Numeric(asdecimal=True))

    quantity = Column(Integer)
    quantity_measure = Column(String(1))
    end_date = Column(DateTime)

    rating_count = Column(Integer, default=0)
    rating_sum = Column(Integer, default=0)

    description = Column(Text)

    us_id = Column(Integer, ForeignKey('users.id'), index=True)
    cat_id = Column(Integer, ForeignKey('categories.id'), index=True)
    loc_id = Column(Integer, ForeignKey('locations.id'), index=True)
    specifics = Column(PGArray(Integer))
    exchange_offers = Column(PGArray(Integer))

    STATE_ACTIVE = 'A'
    STATE_SUSPENDED = 'S'

    KIND_SELL = 'S'
    KIND_EXCHANGE = 'X'
    KIND_COOK = 'G'
    KIND_TEACH = 'T'

    KINDS = {
        KIND_SELL: u'Kupię, sprzedam, oddam, zamienię',
        KIND_COOK: u'Chcę jeść',
        KIND_TEACH: u'Uczę się'
    }

    BARGAIN_SELL = 'S'
    BARGAIN_EXCHANGE = 'X'

    BARGAINS = {
        BARGAIN_SELL: u'Sprzedam',
        BARGAIN_EXCHANGE: u'Wymienię'
    }

    AVAILABILITY_TO_SET = 'U'
    AVAILABILITY_NOW = 'N'
    AVAILABILITY_3DAYS = 'D'
    AVAILABILITY_ONE_WEEK = 'W'
    AVAILABILITY_TWO_WEEKS = 'T'
    AVAILABILITY_UP_TO_MONTH = 'M'
    AVAILABILITY_MORE_THAN_MONTH = 'Y'

    AVAILABILITIES = {
        AVAILABILITY_TO_SET: u'Do uzgodnienia',
        AVAILABILITY_NOW: u'Od ręki',
        AVAILABILITY_3DAYS: u'Do 3 dni roboczych',
        AVAILABILITY_ONE_WEEK: u'W przeciągu tygodnia',
        AVAILABILITY_TWO_WEEKS: u'W przeciągu 2 tygodni',
        AVAILABILITY_UP_TO_MONTH: u'Do miesiąca',
        AVAILABILITY_MORE_THAN_MONTH: u'Powyżej miesiąca'
    }

    AVAILABILITIES_ORDER = [
        AVAILABILITY_TO_SET,
        AVAILABILITY_NOW,
        AVAILABILITY_3DAYS,
        AVAILABILITY_ONE_WEEK,
        AVAILABILITY_TWO_WEEKS,
        AVAILABILITY_UP_TO_MONTH,
        AVAILABILITY_MORE_THAN_MONTH
    ]

    SHIPPING_METHOD_TO_SET = 'U'
    SHIPPING_METHOD_PERSONAL = 'P'
    SHIPPING_METHOD_ONSITE = 'S'
    SHIPPING_METHOD_POST = 'T'
    SHIPPING_METHOD_COURIER = 'C'
    SHIPPING_METHOD_OTHER = 'O'

    SHIPPINGS = {
        SHIPPING_METHOD_TO_SET: u'Do uzgodnienia',
        SHIPPING_METHOD_PERSONAL: u'Odbiór osobisty',
        SHIPPING_METHOD_ONSITE: u'Odbiór na miejscu',
        SHIPPING_METHOD_POST: u'Wysyłka pocztą',
        SHIPPING_METHOD_COURIER: u'Wysyłka kurierem',
        SHIPPING_METHOD_OTHER: u'Inne'
    }

    SHIPPINGS_ORDER = [
            SHIPPING_METHOD_TO_SET,
            SHIPPING_METHOD_PERSONAL,
            SHIPPING_METHOD_ONSITE,
            SHIPPING_METHOD_POST,
            SHIPPING_METHOD_COURIER,
            SHIPPING_METHOD_OTHER
    ]

    QUANTITY_MEASURE_PIECE = 'P'
    QUANTITY_MEASURE_KG = 'K'
    QUANTITY_MEASURE_LITER = 'L'
    QUANTITY_MEASURE_METER = 'M'
    QUANTITY_MEASURE_SACK = 'S'
    QUANTITY_MEASURE_BOX = 'B'

    QUANTITY_MEASURES = {
        QUANTITY_MEASURE_PIECE: 'sztuka',
        QUANTITY_MEASURE_KG: 'kg',
        QUANTITY_MEASURE_LITER: 'litr',
        QUANTITY_MEASURE_METER: 'metr',
        QUANTITY_MEASURE_SACK: 'worek',
        QUANTITY_MEASURE_BOX: 'opakowanie'
    }

    ONE_DAY = 'D'
    THREE_DAYS = 'T'
    WEEK = 'W'
    TWO_WEEKS = 'S'
    MONTH = 'M'
    INFINITY = 'I'

    END_DATES = {
        ONE_DAY: u'jeden dzień (24h)',
        THREE_DAYS: u'trzy dni',
        WEEK: u'tydzień',
        TWO_WEEKS: u'dwa tygodnie',
        MONTH: u'miesiąc',
        INFINITY: u'nieskończoność',
    }

    END_DATES_ORDER = [
        ONE_DAY,
        THREE_DAYS,
        WEEK,
        TWO_WEEKS,
        MONTH,
        INFINITY
    ]

    INFINITY_AS_DATE = datetime.datetime.strptime('1-1-4000', '%d-%m-%Y')

    user = relationship(
        'User',
        backref=backref('products', order_by="Product.name.desc()"))
    location = relationship(
        'Location',
        backref=backref('products', order_by="Location.name.desc()"))
    category = relationship(
        'Category',
        primaryjoin="Category.id==Product.cat_id",
        backref=backref('products', order_by="Product.name.desc()"))

    @classmethod
    def get(cls, pid):
        return DBSession.query(cls).filter(cls.id == pid).first()

    @classmethod
    def get_all(cls):
        return DBSession.query(cls).all()

    @classmethod
    def get_by_category(cls, cat_id, kind=None):
        filters = [
            cls.cat_id == cat_id,
            cls.quantity > 0,
            cls.end_date >= datetime.datetime.now()
        ]
        if kind:
            filters.extend([cls.kind == kind])

        return DBSession.query(cls).filter(and_(*filters)).all()

    @classmethod
    def get_newest(cls, limit=10):
        return DBSession.query(cls).join(Photo).filter(and_(
                        cls.quantity > 0,
                        cls.end_date >= datetime.datetime.now()
                )).order_by(cls.id.desc()).limit(limit).all()

    @classmethod
    def get_all_categories_for_products(cls):
        return Category.get_main()

    def owner_name(self):
        return self.user.user_name()

    def get_coordinated(self):
        return (self.mlang, self.mlong)

    def set_end_date(self, date_state):
        if date_state == self.ONE_DAY:
            self.end_date = datetime.datetime.now() + datetime.timedelta(hours=24)
        elif date_state == self.THREE_DAYS:
            self.end_date = datetime.datetime.now() + datetime.timedelta(hours=3*24)
        elif date_state == self.WEEK:
            self.end_date = datetime.datetime.now() + datetime.timedelta(days=7)
        elif date_state == self.TWO_WEEKS:
            self.end_date = datetime.datetime.now() + datetime.timedelta(days=14)
        elif date_state == self.MONTH:
            self.end_date = datetime.datetime.now() + datetime.timedelta(days=30)
        elif date_state == self.INFINITY:
            self.end_date = self.INFINITY_AS_DATE
        else:
            self.end_date = datetime.datetime.now() + datetime.timedelta(hours=24)

    def until_when_available(self):
        now = datetime.datetime.now()
        if not self.end_date:
            return u'niedostępny'

        diff = self.end_date - now

        if diff.days > 10000:
            return u'bez ograniczeń'

        if diff.days == 1:
            return u'1 dzień'
        elif diff.days > 1:
            return u'%s dni' % (diff.days)

        minutes = int(diff.seconds/60)
        if minutes < 60:
            return u'%s min' % (minutes)
        else:
            return u'%s godz' % (int(minutes/60))

        return now - self.end_date

    @classmethod
    def save_product_for_sale(cls, data, user_id):
        p = Product()
        p.us_id = user_id
        p.name = data.get('title', '-')
        p.cat_id = data.get('category')
        p.subcat_id = data.get('subcategory')
        p.subcat2_id = data.get('subcategory2') or None
        p.kind = data.get('bargain_type')
        p.loc_id = data.get('city')
        p.bargain_type = data.get('bargain_type')
        p.price = data.get('price')
        p.availability = data.get('availability_type')
        p.shipping_method = data.get('shipping_type')
        p.description = data.get('description')
        p.quantity = int(data.get('quantity'))
        p.set_end_date(data.get('end_date'))
        p.specifics = [int(x) for x in data.get('specifics', [])]
        p.quantity_measure = data.get('quantity_measure', 'P')

        if p.loc_id:
            city = Location.get(p.loc_id)
            if city:
                p.localisation = "%s, %s, Polska" % (
                    city.name, city.wojewodztwo.name.lower())

        DBSession.add(p)
        DBSession.flush()
        return p

    def save_edited_product_for_sale(self, data):
        self.name = data.get('title', '-')
        if self.is_product():
            self.cat_id = data.get('category')
            self.subcat_id = data.get('subcategory')
            self.subcat2_id = data.get('subcategory2')
            self.loc_id = data.get('city')
            self.bargain_type = data.get('bargain_type')
            self.price = data.get('price')
            self.availability = data.get('availability_type')
            self.shipping_method = data.get('shipping_type')
            self.quantity = int(data.get('quantity'))
            if data.get('end_date'):
                self.set_end_date(data.get('end_date'))
            if self.loc_id:
                city = Location.get(self.loc_id)
                if city:
                    self.localisation = "%s, %s, Polska" % (
                        city.name, city.wojewodztwo.name.lower())
        self.description = data.get('description')
        DBSession.flush()

    def save_product_photo(self, photo, main=False):
        if type(photo) is type(''): 
            return False

        file_content = photo.file.read()
        if len(file_content) == 0:
            return False

        filename, ext = os.path.splitext(photo.filename)
        filename = unicodedata.normalize('NFD', filename).encode('ascii', 'ignore')
        md5_ = md5(str(file_content)).hexdigest()
        
        new_filename = md5_ + '_' + filename.lower() + ext.lower()
        
        if not os.path.exists(Photo.BASE_STORAGE_PATH + new_filename[0]):
            os.makedirs(Photo.BASE_STORAGE_PATH + new_filename[0])
            
        new_filename_with_path = Photo.BASE_STORAGE_PATH + new_filename[0] + '/' + new_filename
        
        Photo.save_original(new_filename_with_path, file_content)
        
        img = Image.open(new_filename_with_path)
        #if img.mode != "RBG":
        #    img = img.convert("RGB")
            
        maps_image = Photo.resize(img, Photo.MAPS_THUMBNAIL, new_filename, 'maps_')
        tiny_image = Photo.resize(img, Photo.TINY_THUMBNAIL, new_filename, 'tiny_')
        small_image = Photo.resize(img, Photo.SMALL_THUMBNAIL, new_filename, 'small_')
        big_image = Photo.resize(img, Photo.BIG_THUMBNAIL, new_filename, 'big_')
        maxi_image = Photo.resize(img, Photo.MAXI_THUMBNAIL, new_filename, 'maxi_')

        photo = self.save_photo(new_filename_with_path, main=main)
        return photo
        
    def save_photo(self, filepath, main=False):
        photo = Photo()
        photo.filepath = filepath
        photo.product_id = self.id
        photo.is_main = main
        DBSession.add(photo)
        DBSession.flush()
        return photo
        
    def get_main_photo_url(self, photo_type):
        for photo in self.photos:
            if photo.is_main:
                return photo.get_url(photo_type)
        return None
    
    def get_main_photo_object(self):
        for photo in self.photos:
            if photo.is_main:
                return photo
        return None
        
    def get_aside_photo_url(self, photo_type):
        aux = []
        for photo in self.photos:
            if not photo.is_main:
                aux.append(photo.get_url(photo_type))
        return aux

    def get_aside_photo_objects(self):
        aux = []
        for photo in self.photos:
            if not photo.is_main:
                aux.append(photo)
        return aux
        
    def get_first_aside_photo_object(self):
        photos = self.get_aside_photo_objects()
        if len(photos) > 0:
            return photos[0]
        return None

    def get_second_aside_photo_object(self):
        photos = self.get_aside_photo_objects()
        if len(photos) > 1:
            return photos[1]
        return None

    def get_sef_url(self):
        return '/produkt/%s/%s' % (self.id, make_sef_url(self.name))
        
    @classmethod
    def delete_one(cls, product_id):
        p = Product.get(product_id)
        DBSession.delete(p)
        DBSession.flush()
        
    def is_lesson(self):
        return self.kind == self.KIND_TEACH

    def is_food(self):
        return self.kind == self.KIND_COOK
        
    is_dish = is_food
    is_cook = is_food
    
    def is_product(self):
        return self.kind == self.KIND_SELL
        
    @property
    def recommended(self):
        return DBSession.query(Product).join(Photo).filter(
                    Product.id!=self.id
                ).order_by(Product.id.desc()).limit(3).all()
                
    def calculate_grades(self):
        result = DBSession.query(func.avg(Vote.hat_count).label('average')).filter(
            Vote.product_id == self.id
        ).scalar()
        return int(math.ceil(result or 1))
    
    @classmethod
    def get_products_eligible_for_map(cls):
        return DBSession.query(Product).join(Photo).filter(Product.mlang != None).all()

    def decrease_quantity(self, quantity):
        self.quantity -= int(quantity)
        if self.quantity < 0:
            self.quantity = 0
        DBSession.flush()

    def increase_quantity(self, quantity):
        self.quantity += int(quantity)
        if self.quantity < 0:
            self.quantity = 0
        DBSession.flush()

    def html_breadcrumb(self, request):
        category_link = request.route_path(
            'home_show_products',
            id=self.category.id,
            sef=make_sef_url(self.category.name))
        category_href = '<a class="top-shelf" href="%s">%s</a>' % (
            category_link,
            self.category.name)
        return category_href

    def get_specifics(self):
        return DBSession.query(Specifics).filter(
            Specifics.id.in_(self.specifics)).all()

    def get_measure(self):
        measure = self.quantity_measure or self.QUANTITY_MEASURE_PIECE
        return self.QUANTITY_MEASURES[measure]

    def is_mine(self, logged):
        if not logged:
            return
        return logged.id == self.user.id

    @classmethod
    def get_all_by_keyword(cls, keyword):
        return DBSession.query(cls).filter(or_(
                        cls.name.ilike('%%%s%%' % (keyword)),
                        cls.description.ilike('%%%s%%' % (keyword))
                    )).all()
