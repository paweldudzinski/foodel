# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
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

class Message(Base, KJBase):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    when_created = Column(DateTime, default=datetime.datetime.now())
    thread_id = Column(Integer, index=True)
    from_us_id = Column(Integer, ForeignKey('users.id'), index=True)
    to_us_id = Column(Integer, ForeignKey('users.id'), index=True)
    direction = Column(String(2))
    message = Column(Text)
    read = Column(Boolean, server_default="false", nullable=False)
    
    from_us_id = Column(Integer, ForeignKey('users.id'), index=True)
    to_us_id = Column(Integer, ForeignKey('users.id'), index=True)
    thread_id = Column(Integer, ForeignKey('threads.id'), index=True)
    
    sender = relationship('User', primaryjoin="Message.from_us_id==User.id", backref=backref('sender_messages'))
    recipient = relationship('User', primaryjoin="Message.to_us_id==User.id", backref=backref('recipient_messages'))
    thread = relationship('Thread', backref=backref('messages', order_by="Message.id.asc()"))
    
    DIRECTION_OWNER_ASKER = 'OA'
    DIRECTION_ASKER_OWNER = 'AO'
    
    def body(self):
        return self.message
        
    def is_mine(self, user):
        return self.sender == user
        
    def is_read(self):
        return self.read

    def is_unread(self):
        return not self.read
        
    def mark_read(self):
        self.read = True
    
    
    
    
