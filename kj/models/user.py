# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    and_,
    or_,
    )

from ..db import (
    Base,
    KJBase,
    DBSession,
    )

from ..lib.helpers import make_sef_url    
from ..lib.email_sender import EmailSender

from photo import Photo
from product import Product
from message import Message
from thread import Thread
from order import Order

class User(Base, KJBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    
    email = Column(String(258), unique=True)
    password = Column(String(32))
    md5 = Column(String(100))
    
    name = Column(String(1000))
    company = Column(String(1000))
    street = Column(String(1000))
    zip = Column(String(6))
    city = Column(String(1000))
    country = Column(String(1000))
    vat_id = Column(String(1000))
    
    lg_id = Column(String(2), default='pl')
    is_admin = Column(Boolean, default=False)
    
    confirmed = Column(Boolean, default=False)
    
    @classmethod
    def get_by_id(cls, userid):
        return DBSession.query(cls).filter(cls.id == userid).first()
        
    @classmethod
    def get_by_email(cls, email):
        return DBSession.query(cls).filter(cls.email == email).first()
        
    @classmethod
    def get_by_id_and_md5(cls, userid, md5):
        return DBSession.query(cls).filter(and_(cls.id == userid,
                                            cls.md5 == md5)).first()

    @classmethod
    def login(cls, login, password):
        return DBSession.query(cls).filter(and_(cls.email == login,
                                           cls.password == password,
                                           cls.confirmed == True)).first()
                                           
    def user_name(self):
        name = self.name or self.company or self.email
        splitted = name.split(' ')
        if len(splitted) > 0:
            return "%s %s." % (splitted[0], splitted[1][0])
        return name
        
    @classmethod
    def save_new(cls, data, generate_password=False):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        terms_and_conditions = data.get('terms_and_conditions')
        
        user = User()
        user.name = name
        user.email = email
        if generate_password:
            user.password = hashlib.md5(email).hexdigest()[:4]
        else:
            user.password = password
        user.confirmed = generate_password
        user.md5 = hashlib.md5(email).hexdigest()
        DBSession.add(user)
        DBSession.flush()
        
        if not generate_password:
            EmailSender.send_new_user_email(user)
        return user

    def save_edited(self, data):       
        self.name = data.get('name')
        self.password = data.get('password')
        self.company = data.get('company')
        self.vat_id = data.get('vat_id')
        self.street = data.get('street')
        self.zip = data.get('zip')
        self.city = data.get('city')
        
        DBSession.flush()
        
    def confirm(self):
        self.confirmed = True
        DBSession.flush()
        
    def save_avatar(self, filepath):
        photo = Photo()
        photo.filepath = filepath
        photo.us_id = self.id
        DBSession.add(photo)
        DBSession.flush()
        return photo
        
    def get_all_products(self):
        return DBSession.query(Product).filter(and_(
                        Product.us_id == self.id,
                        Product.quantity > 0,
                        Product.end_date >= datetime.now()
                )).all()
                
    def get_products_for_message(self):
        return DBSession.query(Product).filter(and_(
                        Product.us_id == self.id,
                        Product.quantity > 0,
                        Product.end_date >= datetime.now()
                )).limit(8).all()
    
    def get_all_products_for_sale(self):
        return DBSession.query(Product).filter(and_(
                        Product.us_id == self.id,
                        Product.kind == Product.KIND_SELL,
                        Product.quantity > 0,
                        Product.end_date >= datetime.now()
                )).all()

    def get_all_products_for_exchange(self):
        return DBSession.query(Product).filter(and_(
                        Product.us_id == self.id,
                        Product.kind == Product.KIND_EXCHANGE,
                        Product.quantity > 0,
                        Product.end_date >= datetime.now()
                )).all()
    
    def get_product_for_sales_count(self):
        return DBSession.query(Product).filter(and_(
                        Product.us_id == self.id,
                        Product.kind == Product.KIND_SELL,
                        Product.quantity > 0,
                        Product.end_date >= datetime.now()
                )).count()
                
    def get_product_for_exchange_count(self):
        return DBSession.query(Product).filter(and_(
                        Product.us_id == self.id,
                        Product.kind == Product.KIND_EXCHANGE,
                        Product.quantity > 0,
                        Product.end_date >= datetime.now()
                )).count()
    
    def get_number_of_unread_messages(self):
        i = 0
        for m in self.recipient_messages:
            if not m.read:
                i+=1
        return i
        
    def get_number_of_ongoing_events(self):
        return len(self.get_active_events())
        
    def get_active_events(self):
        events = self.events
        now = datetime.now()
        return [event for event in events if event.event_starts >= now]
        
    def get_unactive_events(self):
        events = self.events
        now = datetime.now()
        return [event for event in events if event.event_starts < now]
        
    def get_all_threads(self):
        sql =  """
            SELECT
                DISTINCT th.id,
                th.when_updated
            FROM
                threads th,
                users us
            WHEREevent_ends
                th.from_us_id = %s
                OR th.to_us_id = %s
            ORDER BY th.when_updated DESC;
        """ % (self.id, self.id)
        result = DBSession.execute(sql).fetchall()
        threads = []
        for row in result:
            tid = row[0]
            threads.append(Thread.get(tid))
        return threads
    
    def can_see_message(self, thread_id):
        return DBSession.query(Thread).filter(and_(
                Thread.id == thread_id,
                or_(
                    Thread.from_us_id == self.id,
                    Thread.to_us_id == self.id
                )
            )).first()
        
    def get_sold_new_orders_count(self):
        return DBSession.query(Order).filter(and_(
                        Order.seller_us_id == self.id,
                        Order.seller_status == Order.OS_NEW
                )).count()
                
    def get_bought_new_orders_count(self):
        return DBSession.query(Order).filter(and_(
                        Order.buyer_us_id == self.id,
                        Order.buyer_status == Order.OS_NEW
                )).count()
    
    def get_sold_all_orders_counts_as_dict(self, filters):
        sql = """
            SELECT
                seller_status as status,
                count(id) as count
            FROM
                orders
            WHERE
                seller_us_id = %s
        """ % (self.id)
        
        time = filters['time']
        if time != Order.TIME_INFINITY:
            sql += " AND %s " % (Order.TIME_QUERY_PART[time]['sql'])
        sql+= " GROUP BY status"
        return DBSession.execute(sql)
        
    def get_bought_all_orders_counts_as_dict(self, filters):
        sql = """
            SELECT
                buyer_status as status,
                count(id) as count
            FROM
                orders
            WHERE
                buyer_us_id = %s
        """ % (self.id)
        
        time = filters['time']
        if time != Order.TIME_INFINITY:
            sql += " AND %s " % (Order.TIME_QUERY_PART[time]['sql'])
        sql+= " GROUP BY status"
        return DBSession.execute(sql)
        
    def get_sort_type_sa(self, filters):
        sort_type = filters['type']
        if sort_type == Order.BY_TIME:
            return 'orders.when_created desc'
        else:
            return 'orders.product_id, orders.when_created desc'
        
    def get_bought_orders_by_type(self, type, filters):
        time = filters['time']
        sqla_filters = [Order.buyer_us_id == self.id,
                        Order.buyer_status == type]
        if time != Order.TIME_INFINITY:
            sqla_filters.append(Order.when_created > datetime.today() - Order.TIME_QUERY_PART[time]['sa'])
                
        order_by = self.get_sort_type_sa(filters)
                
        return DBSession.query(Order).filter(and_(*sqla_filters)).order_by(order_by).all()
        
    def get_sold_orders_by_type(self, type, filters):
        time = filters['time']
        sqla_filters = [Order.seller_us_id == self.id,
                        Order.seller_status == type]
        
        if time != Order.TIME_INFINITY:
            sqla_filters.append(Order.when_created > datetime.today() - Order.TIME_QUERY_PART[time]['sa'])
        
        order_by = self.get_sort_type_sa(filters)
        
        return DBSession.query(Order).filter(and_(*sqla_filters)).order_by(order_by).all()
        
    def get_orders_to_grade(self, filters):
        if not filters:
            filters = {}
            filters['time'] = 'Y'
            filters['type'] = 'N'
        orders_not_graded = []
        bought_and_finished = self.get_bought_orders_by_type(Order.OS_FINISHED, filters)
            
        for order in bought_and_finished:
            if not order.is_graded_by_me(self.id, order.product.id):
                orders_not_graded.append(order)
        
        return orders_not_graded
        
    def get_grade(self):
        sql = """
            SELECT avg(v.hat_count)
            FROM votes v JOIN products p ON v.product_id = p.id JOIN users u ON u.id = p.us_id
            WHERE u.id = %s
        """ % (self.id)
        grade = DBSession.execute(sql).fetchall()[0][0]
        return grade and int(round(grade)) or None
        
    def get_active_sender_threads(self):
        threads = DBSession.query(Thread).filter(and_(
                        Thread.from_us_id==self.id
                    )).all()
        active_threads = []
        for t in threads:
            archived = list(t.archived_by or [])
            if self.id not in archived:
                active_threads.append(t)
        return active_threads
                    
    def get_active_recipient_threads(self):
        threads = DBSession.query(Thread).filter(and_(
                        Thread.to_us_id==self.id
                    )).all()
        active_threads = []
        for t in threads:
            archived = list(t.archived_by or [])
            if self.id not in archived:
                active_threads.append(t)
        return active_threads
        
    def get_archived_sender_threads(self):
        threads = DBSession.query(Thread).filter(and_(
                        Thread.from_us_id==self.id
                    )).all()
        archived_threads = []
        for t in threads:
            archived = list(t.archived_by or [])
            if self.id in archived:
                archived_threads.append(t)
        return archived_threads
                    
    def get_archived_recipient_threads(self):
        threads = DBSession.query(Thread).filter(and_(
                        Thread.to_us_id==self.id
                    )).all()
        archived_threads = []
        for t in threads:
            archived = list(t.archived_by or [])
            if self.id in archived:
                archived_threads.append(t)
        return archived_threads
        
    def profile_link(self, request):
        return request.route_path('profile_link', id=self.id, sef=make_sef_url(self.user_name()))
        
        
        
        
        
        
        
        
