from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid

from pygeocoder import Geocoder

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class RootFactory(object):
    __acl__ = [
        (Allow, 'user', ALL_PERMISSIONS),
        (Allow, 'admin', ALL_PERMISSIONS)
    ]
    
    def __init__(self, request):
        self.request = request

class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        from .models.user import User
        userid = unauthenticated_userid(self)
        if self.path.startswith('/admin'):
            return User.admin_by_id(userid)
        if userid is not None:
            return User.get_by_id(userid)
            
class KJBase(object):
    
    def __init__(self, *args, **kwargs):
        self.fill_with_kwargs(*args, **kwargs)
    
    @classmethod
    def get(cls, object_id):
        return DBSession.query(cls).filter(cls.id == object_id).first()
        
    @classmethod
    def all(cls):
        return DBSession.query(cls).all()
        
    def fill_with_kwargs(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            if v not in (None, ''):
                setattr(self, k, v)
        return self
        
    def save_geolocalisation(self):
        if not hasattr(self, 'localisation'):
            return
            
        if not hasattr(self, 'street'):
            results = Geocoder.geocode(self.localisation)
        else:
            results = Geocoder.geocode("%s, %s" % (self.street, self.localisation))
            
            
        if not results:
            return
        
        coords = results[0].coordinates
        self.mlang = coords[0]
        self.mlong = coords[1]
        
        DBSession.flush()
    
    def is_eligible_for_map(self):
        return self.mlang
