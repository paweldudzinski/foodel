# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    and_,
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

class Location(Base, KJBase):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    lg_id = Column(String(2), default='pl')
    name = Column(String(2000))
    woj_id = Column(Integer, ForeignKey('locations.id'), index=True)
    
    @classmethod
    def get_main(cls, lg_id = 'pl'):
        return DBSession.query(cls).filter(and_(cls.lg_id == lg_id,
                                            cls.woj_id == None)).order_by(cls.name).all()
                                        
Location.cities = relationship(
    'Location',
    backref=backref('wojewodztwo',
                   remote_side=[Location.__table__.c.id]), 
                   lazy='joined', join_depth=2,
                   order_by=[Location.__table__.c.name.asc()])
                   
    
