# -*- coding: utf-8 -*-
from ..models.email_queue import EmailQueue
from ..models.product import Product

class EmailSender(object):
    
    FROM = 'Foodel.pl <info@foodel.pl>'
    TYPE_REGISTER_EMAIL = 'R'
    TYPE_MESSAGE_RECEIVED = 'M'
    TYPE_PRODUCT_BOUGHT = 'B'

    @classmethod
    def send_new_user_email(cls, user):
        subject = u'Witamy na pokladzie Foodel.pl!'
        msg  = u"""Żeby potwierdzić rejestrację, proszę wejdź w poniższy link:<br />
            <b>http://www.foodel.pl/potwierdz/%s/%s</b><br />
            Dzięki z gory!<br />
            ---<br />
            Foodel.pl
        """ % (user.id, user.md5)

        EmailQueue.push(cls.TYPE_REGISTER_EMAIL, user, subject, msg.strip())

    @classmethod
    def send_you_have_a_new_message_email(cls, message):
        subject = u'Dostałeś nową wiadomość od użytkownika Foodla!'
        msg = u"""Dostałeś wiadomość od %s (%s) dotyczącą produktu <b>%s</b>.<br />
            Możesz ją przeczytać tu:
            http://www.foodel.pl/wiadomosc/%s#last_or_new<br />
            Pozdrawiamy!<br />
            ---<br />
            Foodel.pl<br />
        """ % (message.recipient.user_name(),
               message.recipient.email,
               message.thread.product.name,
               message.thread.id)
               
        EmailQueue.push(cls.TYPE_MESSAGE_RECEIVED, message.recipient, subject, msg.strip())

    @classmethod
    def send_product_bought_email(cls, buyer, product):
        subject = u'Ktoś zainteresował się Twoim produktem na Foodlu!'
        
        action = u'wymienić się' if product.kind == Product.KIND_EXCHANGE else u'kupić'
        
        msg = u"""
            Użytkownik %s (%s) chciałby %s twój przedmiot:<br />
            <b>%s</b>.<br />
            Wejdź w poniższy link i zobacz o co chodzi:<br />
            http://www.foodel.pl/moja-sprzedarz/zakonczone<br />
            Pozdrawiamy!<br />
            ---<br />
            Foodel.pl<br />
        """ % (buyer.user_name(),
               buyer.email,
               action,
               product.name)
        
        EmailQueue.push(cls.TYPE_PRODUCT_BOUGHT, product.user, subject, msg.strip())
        
        
        
        
        
        
        
        
        
