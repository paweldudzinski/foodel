# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
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
    
class Vote(Base, KJBase):
    __tablename__ = 'votes'
    
    id = Column(Integer, primary_key=True)
    us_id = Column(Integer, ForeignKey('users.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    hat_count = Column(Integer, default=0)
    
    product = relationship('Product', backref=backref('product_votes'))
    user = relationship('User', backref=backref('user_votes'))
    
   
    
    

