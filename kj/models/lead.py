# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    )
    
from ..db import (
    Base,
    KJBase,
    DBSession,
    )
    
class Lead(Base, KJBase):
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    email = Column(String(200))
    phone = Column(String(200))
    category = Column(String(1))
    description = Column(String(5000))
    
    LC_FOOD_PRODUCERS = 'P'
    LC_BLOGGERS = 'B'
    LC_PRESS = 'G'

    LC_NAMES = {
        LC_FOOD_PRODUCERS: 'Producenci jedzenia',
        LC_BLOGGERS: 'Blogerzy kulinarni',
        LC_PRESS: 'Prasa kulinarna'
    }

    @classmethod
    def save(cls, name, email, phone, description, category):
        lead = Lead()
        lead.name = name
        lead.email = email
        lead.phone = phone
        lead.description = description
        lead.category = category
        DBSession.add(lead)
        DBSession.flush()
        return lead
        
    def update(self, name, email, phone, description, category):
        self.name = name
        self.email = email
        self.phone = phone
        self.description = description
        self.category = category
        DBSession.flush()
        return self
        
    @classmethod
    def delete(cls, lead_id):
       lead = Lead.get(lead_id)
       DBSession.delete(lead)
       DBSession.flush()
       
    def get_category_as_text(self):
        return self.LC_NAMES.get(self.category) or '-'
    
    

