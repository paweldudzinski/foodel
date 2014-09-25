# -*- coding: utf-8 -*-
import logging
import datetime

from smtplib import SMTP

class Mailer():
    #SMTP_HOST = "smtp.gmail.com."
    #SMTP_LOGIN = "paweldudzinski@gmail.com"
    #SMTP_PASSWORD = "ImanZoel666"
    #FROM_ADDRESS = "paweldudzinski@gmail.com"
    
    SMTP_HOST = "smtp.mydevil.net"
    SMTP_LOGIN = "kontakt@foodel.pl"
    SMTP_PASSWORD = "xWmnCtoV"
    FROM_ADDRESS = "info@foodel.pl"
    
    
    HEADER_CHARSET = 'UTF-8'
    BODY_CHARSET = 'UTF-8'
    server = None
    
    def __init__(self):
        self.server = SMTP(self.SMTP_HOST)
        
    def login(self):
        self.server.starttls()
        self.server.login(self.SMTP_LOGIN,self.SMTP_PASSWORD)
        
    def quit(self):
        self.server.quit()
        
    def send(self, send_from, send_to, subject, body):
        import email as kj_email
        from email.Utils import parseaddr as kj_parseaddr
        from email.Utils import formataddr as kj_formataddr

        bc = None
        body.encode(self.BODY_CHARSET)

        # Split real name (which is optional) and email address parts
        sender_name, sender_addr = kj_parseaddr(send_from)
        recipient_name, recipient_addr = kj_parseaddr(send_to)

        # We must always pass Unicode strings to Header, otherwise it will
        # use RFC 2047 encoding even on plain ASCII strings.
        sender_name = str(kj_email.Header.Header(unicode(sender_name), self.HEADER_CHARSET))
        recipient_name = str(kj_email.Header.Header(unicode(recipient_name), self.HEADER_CHARSET))
            
        # Make sure email addresses do not contain non-ASCII characters
        sender_addr = sender_addr.encode('ascii')
        recipient_addr = recipient_addr.encode('ascii')

        if bc:
            __body = kj_email.MIMEText.MIMEText(body.encode(bc), 'plain', bc)
        else:
            __body = body
        __from = kj_formataddr((sender_name, sender_addr))
        __to = kj_formataddr((recipient_name, recipient_addr))
        __subject = kj_email.Header.Header(unicode(subject), self.HEADER_CHARSET)
        __date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

        msg = kj_email.MIMEText.MIMEText(__body.encode('utf-8'), 'html', 'utf-8')
        msg['Subject'] = __subject
        msg['From'] = __from
        msg['To'] = __to

        self.server.sendmail(self.FROM_ADDRESS, __to, msg.as_string())
