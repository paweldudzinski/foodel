# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime,
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


class Comment(Base, KJBase):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comment = Column(String(1000), index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    us_id = Column(Integer, ForeignKey('users.id'))
    when_created = Column(DateTime, default=datetime.datetime.now())

    product = relationship(
        'Product',
        backref=backref(
            'comments',
            order_by="Comment.when_created.desc()",
            lazy='dynamic'))
    user = relationship('User')

    @classmethod
    def add(cls, product, comment, user):
        c = Comment(comment=comment,
                    us_id=user.id)
        product.comments.append(c)

    def delete(self):
        DBSession.delete(self)
        DBSession.flush()

    def is_owners(self, product):
        return product.us_id == self.us_id

    def details(self):
        return "dodany %s przez %s" % (
            self.when_created.strftime('%d/%m/%Y %H:%M'),
            self.user.user_name())
