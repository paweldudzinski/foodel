# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
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

from ..models.thread import Thread
from ..models.vote import Vote


class Order(Base, KJBase):
    __tablename__ = 'orders'

    OS_NEW = 'N'
    OS_CANCELLED = 'C'
    OS_FINISHED = 'F'

    ORDER_TO_URL = {
        'nowe': OS_NEW,
        'zakonczone': OS_FINISHED,
        'anulowane': OS_CANCELLED
    }

    ORDER_TO_NAME = {
        OS_NEW: 'nowe',
        OS_FINISHED: u'zakończone',
        OS_CANCELLED: 'anulowane'
    }

    ALLOWED_TYPES = ['nowe', 'zakonczone', 'anulowane']
    ORDER_BOUGHT_SELECT = [
        (OS_NEW, u'Nie dogadaliśmy się, przywróć'),
        (OS_FINISHED, u'Dogadaliśmy się, zakończ'),
        (OS_CANCELLED, u'Anuluj')]
    ORDER_SOLD_SELECT = [
        (OS_NEW, u'Nie dogadaliśmy się, przywróć'),
        (OS_FINISHED, u'Dogadaliśmy się, zakończ'),
        (OS_CANCELLED, u'Anuluj')]

    # ORDER FILTERS

    TIME_WEEK = 'W'
    TIME_MONTH = 'M'
    TIME_THREE_MONTHS = 'T'
    TIME_YEAR = 'Y'
    TIME_INFINITY = 'I'

    TIMES = {
        TIME_WEEK: u'ostatni tydzień',
        TIME_MONTH: u'ostatni miesiąc',
        TIME_THREE_MONTHS: u'trzy miesiące',
        TIME_YEAR: u'rok',
        TIME_INFINITY: u'pokaż wszystkie'
    }

    TIMES_SORTED = [TIME_WEEK, TIME_MONTH, TIME_THREE_MONTHS,
                    TIME_YEAR, TIME_INFINITY]

    TIME_QUERY_PART = {
        TIME_WEEK : {
            'sql' : "when_created > now() - INTERVAL '1 WEEKS'",
            'sa' : relativedelta(weeks=1)
        },
        TIME_MONTH : {
            'sql' : "when_created > now() - INTERVAL '1 MONTH'",
            'sa' : relativedelta(months=1)
        },
        TIME_THREE_MONTHS : {
            'sql' : "when_created > now() - INTERVAL '3 MONTH'",
            'sa' : relativedelta(months=3)
        },
        TIME_YEAR : {
            'sql' : "when_created > now() - INTERVAL '1 YEAR'",
            'sa' : relativedelta(years=1)
        },
    }
    
    BY_TIME = 'T'
    BY_PRODUCT = 'P'
    
    TYPE_SORTED = {
        BY_TIME : u'czasie',
        BY_PRODUCT : u'nazwie produktu'
    }
    
    TYPE_SORTED_SORTED = [BY_TIME, BY_PRODUCT]
    
    id = Column(Integer, primary_key=True)
    when_created = Column(DateTime, default=datetime.datetime.now())
    quantity = Column(Integer)
    
    buyer_status = Column(String(1), default=OS_NEW)
    seller_status = Column(String(1), default=OS_NEW)
    
    thread_id = Column(Integer, ForeignKey('threads.id'), index=True)
    seller_us_id = Column(Integer, ForeignKey('users.id'), index=True)
    buyer_us_id = Column(Integer, ForeignKey('users.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    
    product = relationship('Product')
    seller = relationship('User', primaryjoin="Order.seller_us_id==User.id")
    buyer = relationship('User', primaryjoin="Order.buyer_us_id==User.id")
    thread = relationship('Thread', backref=backref('order'))
    
    @classmethod
    def new(cls, seller=None, buyer=None, product=None, quantity=None, message=None):
        if message:
            msg = '\n%s' % (message)
        else:
            msg = u'%s! Mam to!' % (product.name)
            
        thread = Thread.find_by_sender_and_recipient_and_product(buyer.id, seller.id, product.id)
        if not thread:
            thread = Thread()
            thread.from_us_id = buyer.id
            thread.to_us_id = seller.id
            thread.product_id = product.id
            DBSession.add(thread)
            DBSession.flush()
        
        thread.add_message(buyer.id, seller.id, msg, send_email=False)        
        DBSession.flush()
        
        o = Order()
        o.seller_us_id = seller.id
        o.buyer_us_id = buyer.id
        o.product_id = product.id
        o.thread_id = thread.id
        o.quantity = quantity

        DBSession.add(o)
        DBSession.flush()
        
        return o
        
    def mark(self, status, user_id):
        if self.buyer_us_id == user_id:
            self.buyer_status = status
        else:
            self.seller_status = status
        DBSession.flush()
        
    def get_bought_selects(self):
        if self.buyer_status == self.OS_NEW:
            return self.ORDER_BOUGHT_SELECT[1:]
        elif self.buyer_status == self.OS_FINISHED:
            return self.ORDER_BOUGHT_SELECT[0:3:2]
        else:
            return self.ORDER_BOUGHT_SELECT[:2]

    def get_sold_selects(self):
        if self.seller_status == self.OS_NEW:
            return self.ORDER_SOLD_SELECT[1:]
        elif self.seller_status == self.OS_FINISHED:
            return self.ORDER_SOLD_SELECT[0:3:2]
        else:
            return self.ORDER_SOLD_SELECT[:2]
    
    def is_graded_by_me(self, us_id, product_id):
        return DBSession.query(Vote).filter(and_(
            Vote.us_id == us_id,
            Vote.product_id == product_id
        )).first()
        
    def can_grade_order(self, us_id):
        if self.is_graded_by_me(us_id, self.product.id):
            return False
            
        return self in self.buyer.get_orders_to_grade([])
        
    def grade(self, grade):
        v = Vote()
        v.us_id = self.buyer.id
        v.product_id = self.product.id
        v.hat_count = int(grade)
        DBSession.add(v)
        DBSession.flush()
        return v
        
        
        
        

