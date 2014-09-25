# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    Integer,
    String,
    and_,
    )

from ..db import (
    Base,
    KJBase,
    DBSession,
    )

class Specifics(Base, KJBase):
    __tablename__ = 'specifics'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
                   
    
