# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    Boolean,
    and_,
    )
    
from sqlalchemy.orm import (
    relationship,
    backref,
    )

from ..db import (
    Base,
    DBSession,
    )

import os
import copy
from PIL import Image

class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    filepath = Column(String(2000))
    is_main = Column(Boolean, default=False)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    us_id = Column(Integer, ForeignKey('users.id'), index=True)
    event_id = Column(Integer, ForeignKey('events.id'), index=True)
    
    product = relationship('Product', backref=backref('photos'))
    user = relationship('User', backref=backref('avatars'))
    event = relationship('Event', backref=backref('event_photos'))
    
    BASE_STORAGE_PATH = 'kj/static/storage/'
    AVATAR_THUMBNAIL = 50
    MAPS_THUMBNAIL = 50
    TINY_THUMBNAIL = 150
    SMALL_THUMBNAIL = 240
    BIG_THUMBNAIL = 500
    MAXI_THUMBNAIL = 800
    
    PREFIXES = [None, 'avatar_','tiny_','small_','big_','maxi_', 'maps_']

    @classmethod
    def get_by_id(cls, stid):
        return DBSession.query(cls).filter(cls.id == stid).first()
    
    @classmethod
    def save_photo(cls, new_filename_with_path, product_id):
        photo = Storage()
        photo.filepath = new_filename_with_path
        photo.product_id = product_id
        DBSession.add(photo)
        DBSession.flush()
        return photo
    
    @classmethod
    def save_original(cls, new_filename_with_path, file_content):
        f = open(new_filename_with_path,'w+')
        f.write(file_content)
        f.close()
        
    @classmethod
    def delete_one(cls, photo):
        DBSession.delete(photo)
        DBSession.flush()
        
    @classmethod
    def resize(cls, img, new_size, new_filename, prefix):
        image_to_resize = copy.copy(img)
        width, height = image_to_resize.size
        
        if height >= new_size:
            tiny_thumbnail_width = (width * new_size)/height
            image_to_resize.thumbnail((tiny_thumbnail_width, new_size), Image.ANTIALIAS)
            
        if width >= new_size:
            tiny_thumbnail_height = (height * new_size)/width
            image_to_resize.thumbnail((new_size, tiny_thumbnail_height), Image.ANTIALIAS)
            
        image_to_resize.save(cls.BASE_STORAGE_PATH + new_filename[0] + '/' + prefix + new_filename)
        
        return image_to_resize
        
    def get_url(self, prefix=None):
        if prefix:
            splitted_path = self.filepath.split('/')
            with_prefix = prefix + splitted_path[-1:][0]
            with_prefix = self.filepath.replace(splitted_path[-1:][0], with_prefix)
            return with_prefix.replace('kj/','/').replace(' ','%20')
        else:
            return self.filepath.replace('kj/','/').replace(' ','%20')
        
