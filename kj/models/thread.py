# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    and_,
    )

from sqlalchemy.orm import (
    relationship,
    backref,
    )
    
from sqlalchemy.dialects.postgresql import ARRAY as PGArray

from ..lib.email_sender import EmailSender

from ..db import (
    Base,
    KJBase,
    DBSession,
    )
    
from message import Message

class Thread(Base, KJBase):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True)
    when_created = Column(DateTime, default=datetime.datetime.now())
    when_updated = Column(DateTime, default=datetime.datetime.now())
    
    from_us_id = Column(Integer, index=True)
    to_us_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    
    from_us_id = Column(Integer, ForeignKey('users.id'), index=True)
    to_us_id = Column(Integer, ForeignKey('users.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    
    archived_by = Column(PGArray(Integer), default=[])

    sender = relationship('User', primaryjoin="Thread.from_us_id==User.id", backref=backref('all_sender_threads'))
    recipient = relationship('User', primaryjoin="Thread.to_us_id==User.id", backref=backref('all_recipient_threads'))
    product = relationship('Product', backref=backref('threads'))
    
    @classmethod
    def find_by_sender_and_recipient_and_product(cls, sid, rid, pid):
        return DBSession.query(cls).filter(and_(
                    cls.from_us_id == sid,
                    cls.to_us_id == rid,
                    cls.product_id == pid
                )).first()
    
    def get_direction(self, sid):
        asker = self.from_us_id
        if asker == sid:
            return Message.DIRECTION_ASKER_OWNER
        else:
            return Message.DIRECTION_OWNER_ASKER
         
    def add_message(self, sid, rid, msg, send_email=True):
        message = Message()
        message.thread = self
        message.from_us_id = sid
        message.to_us_id = rid
        message.message = msg
        message.direction = self.get_direction(sid)
        self.when_updated = datetime.datetime.now()
        DBSession.add(message)
        DBSession.flush()
        if send_email:
            EmailSender.send_you_have_a_new_message_email(message)
        return message
        
    def get_unread_messages(self, user):
        unread = []
        for message in self.messages:
            if message.to_us_id == user.id and not message.read:
                unread.append(message)
        return unread
        
    def is_mine(self, user):
        return self.sender == user
        
    def archive(self, user):
        user_archived = list(self.archived_by or [])
        if user.id not in user_archived:
            user_archived.append(user.id)
            self.archived_by = user_archived
            DBSession.flush()
        
    def is_archived(self, user):
        user_archived = list(self.archived_by or [])
        return user.id in user_archived
        
        
        
        
        
        
        
        
        
        
