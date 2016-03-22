# -*- coding: utf-8 -*-
import datetime

from random import randint
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
from ..lib.geo import geo

from sqlalchemy.dialects.postgresql import ARRAY as PGArray


class Category(Base, KJBase):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    lg_id = Column(String(2), default='pl')
    name = Column(String(2000))
    parent_id = Column(Integer, ForeignKey('categories.id'), index=True)
    coupled = Column(PGArray(Integer))

    @classmethod
    def get_main(cls, lg_id='pl'):
        return DBSession.query(cls).filter(
            and_(
                 cls.lg_id == lg_id, cls.parent_id == None  # noqa
                 )
            ).order_by(cls.name).all()

    @classmethod
    def get_main_with_product_ids(
            cls,
            lg_id='pl',
            where_statement='',
            keyword=None,
            product_specific=None):
        from ..models.product import Product
        sql = """
            SELECT cat.id as id, cat.name as name, array_agg(prod.id) as prods
            FROM categories cat JOIN products prod ON cat.id = prod.cat_id
            WHERE
                cat.parent_id is null %s
                AND prod.quantity > 0
                AND prod.end_date >= '%s'
            GROUP BY cat.id
        """ % (where_statement, datetime.datetime.now())
        output = {}
        result = DBSession.execute(sql).fetchall()
        for r in result:
            products = DBSession.query(Product).filter(
                Product.id.in_(r.prods)).order_by(Product.id.desc()).limit(4).all()
            products = geo.filter_products(products, keyword, product_specific)
            if not products:
                continue
            display_product_idx = randint(0, len(products)-1)
            output[r.id] = {
                'name': r.name,
                'product': products[display_product_idx],
                'counter': len(products),
                'category': Category.get(r.id)
            }
        return output

    def get_subs_product_ids(self, lg_id='pl', where_statement=''):
        from ..models.product import Product
        sql = """
            SELECT cat.id as id, cat.name as name, array_agg(prod.id) as prods
            FROM categories cat JOIN products prod ON cat.id = prod.subcat_id
            WHERE 
                cat.parent_id = %d %s
                AND prod.quantity > 0
                AND prod.end_date >= '%s'
            GROUP BY cat.id
        """ % (self.id, where_statement, datetime.datetime.now())
        output = {}
        result = DBSession.execute(sql).fetchall()
        for r in result:
            products = DBSession.query(Product).filter(Product.id.in_(r.prods)).order_by(Product.id.desc()).all()
            count_sql = """
                    SELECT count(prod.id) 
                    FROM products prod
                    WHERE 
                        (prod.subcat_id = %s OR prod.subcat2_id = %s)
                        AND prod.quantity > 0 %s 
                        AND prod.end_date >= '%s'
            """ % (r.id, r.id, where_statement, datetime.datetime.now())
            output[r.id] = {
                'name': r.name,
                'products': products[:4],
                'counter': DBSession.execute(count_sql).scalar()
            }
        return output

    def get_current_with_product_ids(self, lg_id='pl', where_statement=''):
        from ..models.product import Product
        sql = """
            SELECT cat.id as id, cat.name as name, array_agg(prod.id) as prods
            FROM categories cat JOIN products prod ON cat.id = prod.subcat_id
            WHERE 
                cat.id = %d %s
                AND prod.quantity > 0
                AND prod.end_date >= '%s'
            GROUP BY cat.id
        """ % (self.id, where_statement, datetime.datetime.now())
        output = {}
        result = DBSession.execute(sql).fetchall()
        for r in result:
            products = DBSession.query(Product).filter(Product.id.in_(r.prods)).order_by(Product.id.desc()).all()
            count_sql = """
                    SELECT count(prod.id) 
                    FROM products prod 
                    WHERE 
                        (prod.subcat_id = %s OR prod.subcat2_id = %s)
                        AND prod.quantity > 0
                        AND prod.end_date >= '%s'
            """ % (r.id, r.id, datetime.datetime.now())
            output[r.id] = {
                'name': r.name,
                'products': products[:4],
                'counter': DBSession.execute(count_sql).scalar()
            }
        return output
                                    
    @classmethod
    def add_new(cls, parent_category_id, category_name, lg_id = 'pl'):
        cat = Category()
        cat.parent_id = parent_category_id
        cat.name = category_name
        cat.lg_id = lg_id
        DBSession.add(cat)
        DBSession.flush()
        
    @classmethod
    def get_all_as_dict(cls, lg_id = 'pl'):
        main_categories = cls.get_main(lg_id=lg_id)
        as_dict = {}
        for cat in main_categories:
            as_dict[cat.id] = {
                'object' : cat,
                'children' : []
            }
            for subcat in cat.children:
                as_dict[cat.id]['children'].append(subcat)
        return as_dict
        
    @classmethod
    def delete_one(cls, catid):
        cat = Category.get_by_id(catid)
        DBSession.delete(cat)
        DBSession.flush()
        
    @classmethod
    def update_name(cls, id, model_name):
        model = Category.get_by_id(id)
        model.name = model_name
        DBSession.flush()
        
    @classmethod
    def get_not_coupled(cls):
        return DBSession.query(cls).filter(and_(
                            cls.coupled == None,
                            cls.parent_id != None
                        )).order_by(cls.id).all()
                        
    @classmethod
    def get_coupled(cls):
        return DBSession.query(cls).filter(and_(
                            cls.coupled != None,
                            cls.parent_id != None
                        )).order_by(cls.id).all()
                        
    @classmethod
    def get_for_coupling(cls):
        return DBSession.query(cls).filter(
                            cls.parent_id != None
                        ).order_by(cls.id).all()
    
    @property
    def coupled_categories(self):
        if not self.coupled:
            return []
        return DBSession.query(Category).filter(
                            Category.id.in_(self.coupled)
                        ).order_by(Category.id).all()
        

Category.children = relationship(
    'Category',
    backref=backref('parent',
                   remote_side=[Category.__table__.c.id]), 
                   lazy='joined', join_depth=2,
                   order_by=[Category.__table__.c.name.asc()])
                   
    
