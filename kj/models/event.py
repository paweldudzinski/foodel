# -*- coding: utf-8 -*-
import datetime
import os
import unicodedata
from PIL import Image

from hashlib import md5
from kj.lib.helpers import make_sef_url

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Text,
    String
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
    
from photo import Photo
from location import Location
    
class Event(Base, KJBase):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    us_id = Column(Integer, ForeignKey('users.id'), index=True)
    loc_id = Column(Integer, ForeignKey('locations.id'), index=True)
    street = Column(String(1000))
    when_created = Column(DateTime, default=datetime.datetime.now())
    event_starts = Column(DateTime)
    event_ends = Column(DateTime)
    event_time = Column(String(5))
    title = Column(String(1000))
    description = Column(Text)
    localisation = Column(String(1000))
    facebook_url = Column(String(1000))
    
    mlang = Column(String(100))
    mlong = Column(String(100))
    
    location = relationship('Location', backref=backref('events', order_by="Location.name.desc()"))
    user = relationship('User', backref=backref('events'))
    
    @classmethod
    def get_all_active(cls):
        now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
        return DBSession.query(Event).filter(
            Event.event_starts >= now).order_by(
                Event.event_starts).all()
    
    @classmethod
    def create(cls, us_id, title, description, date_from, date_to, 
               loc_id, street, start_hour, start_minute, facebook_url):
        e = Event()
        e.us_id = us_id
        e.title = title
        e.description = description
        e.event_starts = datetime.datetime.strptime(date_from, '%d-%m-%Y')
        e.event_ends = date_to and datetime.datetime.strptime(date_to, '%d-%m-%Y') or None
        e.loc_id = loc_id
        e.facebook_url = facebook_url
        e.street = street
        e.event_time = '%s:%s' % (start_hour, start_minute)
        
        if e.loc_id:
            city = Location.get(e.loc_id)
            if city:
                e.localisation = "%s, %s, Polska" % (city.name, city.wojewodztwo.name.lower())
        
        DBSession.add(e)
        DBSession.flush()
        return e
    
    def save_event_photo(cls, event_id, photo):
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
        if img.mode != "RBG":
            img = img.convert("RGB")
        
        tiny_image = Photo.resize(img, Photo.TINY_THUMBNAIL, new_filename, 'tiny_')
        small_image = Photo.resize(img, Photo.SMALL_THUMBNAIL, new_filename, 'small_')
        big_image = Photo.resize(img, Photo.BIG_THUMBNAIL, new_filename, 'big_')
        maxi_image = Photo.resize(img, Photo.MAXI_THUMBNAIL, new_filename, 'maxi_')

        photo = Photo()
        photo.filepath = new_filename_with_path
        photo.event_id = event_id
        photo.is_main = True
        DBSession.add(photo)
        DBSession.flush()
        return photo
        
    def delete(self):
        DBSession.delete(self)
        DBSession.flush()
        
    def is_mine(self, logged):
        if not logged:
            return
        return logged.id == self.user.id
        
    def get_photo_url(self, photo_type):
        if not self.event_photos:
            return None
        else:
            return self.event_photos[0].get_url(photo_type)
    
    def get_photo_object(self):
        if not self.event_photos:
            return None
        else:
            return self.event_photos[0]

    def get_sef_url(self):
        return '/wydarzenie/%s/%s' % (self.id, make_sef_url(self.title))
    
    def get_main_photo_url(self, photo_type):
        photo = self.event_photos[0] if self.event_photos else None
        return photo and photo.get_url(photo_type)
    
    def get_main_photo_object(self):
        return self.event_photos[0] if self.event_photos else None
