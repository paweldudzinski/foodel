# -*- coding: utf-8 -*-
import datetime
import transaction

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    )
    
from sqlalchemy.orm import (
    relationship,
    )
    
from ..db import (
    Base,
    KJBase,
    DBSession,
    )

from ..lib.mailer import Mailer
    
class EmailQueue(Base, KJBase):
    __tablename__ = 'email_queue'
    
    id = Column(Integer, primary_key=True)
    when_sent = Column(DateTime)
    type = Column(String(2))
    email_to = Column(String(200))
    subject = Column(String(500))
    body = Column(String(5000))
    
    us_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User')
    
    @classmethod
    def push(cls, type, user, subject, body):
        email = EmailQueue()
        email.us_id = user.id
        email.type = type
        email.email_to = user.email
        email.subject = subject
        email.body = body 
        DBSession.add(email)
        DBSession.flush()
        return email
    
    @classmethod
    def get_emails_to_send(cls):
        return DBSession.query(cls).filter(cls.when_sent == None).all()
        
    def send(self):
        from ..models.user import User
        from ..lib.email_sender import EmailSender
        mailer = Mailer()
        mailer.login()
        mailer.send(EmailSender.FROM, self.user.email, self.subject, self.body)
        self.mark_sent()
        
    def mark_sent(self):
        self.when_sent = datetime.datetime.now()
        transaction.commit()
    
    

