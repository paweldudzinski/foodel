# -*- coding: utf-8 -*-
from kj.models.product import Product
from kj.models.specifics import Specifics
from kj.models.location import Location


class ProductCreator(object):

    def __init__(self):
        self.bargain_values = tuple(Product.BARGAINS.iteritems())
        self.availabilility_values = [(a, Product.AVAILABILITIES[a]) for a in Product.AVAILABILITIES_ORDER]
        self.shipping_values = [(a, Product.SHIPPINGS[a]) for a in Product.SHIPPINGS_ORDER]
        self.end_date_values = [(a, Product.END_DATES[a]) for a in Product.END_DATES_ORDER]
        self.categories = [(a.id, a.name) for a in Product.get_all_categories_for_products()]
        self.quantity_measures = [(a, Product.QUANTITY_MEASURES[a]) for a in Product.QUANTITY_MEASURES]
        self.specifics = Specifics.all()
        self.wojewodztwa = [(a.id, a.name) for a in Location.get_main()]

product_creator = ProductCreator()
