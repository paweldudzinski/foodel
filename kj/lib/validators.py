# -*- coding: utf-8 -*-
import re


class Validator(object):

    @classmethod
    def validate(cls, data):
        pass


class ValidateEmail(Validator):

    def __init__(self, email):
        self.email = email

    def check(self):
        return re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", self.email)


class ZipCodeValidator(Validator):

    @classmethod
    def validate(cls, data):
        return re.match(r"^[0-9]{2}-[0-9]{3}$", data)


class NewUserValidator(Validator):

    @classmethod
    def validate(cls, data):
        email = data.get('email')
        password = data.get('password')
        rpassword = data.get('rpassword')
        terms_and_conditions = data.get('terms_and_conditions')
        required = ['name', 'email', 'password', 'rpassword', 'terms_and_conditions']

        for k, v in data.iteritems():
            if not v and k in required:
                return False
        if not terms_and_conditions:
            return False

        if password != rpassword:
            return False

        if not ValidateEmail(email).check():
            return False

        return True
