# -*- coding: utf-8 -*-
import re
import webhelpers.paginate as paginate

def make_sef_url(part, accept_numbers=False):
	""" Robi linki google friendly """
	
	if not type(part) is unicode:
		part = part.decode('utf8')
	
	import unicodedata
	part = part.replace(u"ł", "l").replace(u"Ł", "l")
	part = unicodedata.normalize ('NFKD', part).encode ('ASCII', 'ignore') 
	part = part.lower()
	if not accept_numbers:
		part = re.sub('([^a-zA-Z\s])', " ", part)
	else:
		part = re.sub('([^0-9a-zA-Z\s])', " ", part)
	part = re.sub('\s{2,}', " ", part)
	part = part.strip().replace(" ", "_")
	return part
    
def smart_truncate(content, length, splitter=' '):
    if len(content) <= length:
        return content
    else:
        return "%s..."%(splitter.join(content[:length + 1].split(splitter)[0:-1]))

def email_truncate(email, length):
    if len(email) > length:
        return "%s..." % (email[:length])
    return email

def chunk(q, request):
    page_url = paginate.PageURL_WebOb(request)
    current_page = int(request.params.get('page', 0))
    return paginate.Page(q, current_page, url=page_url, items_per_page=30)
    
def get_pl_weekday(date):
    weekday = date.weekday()
    if weekday == 0:
        return u'poniedziałek'
    elif weekday == 1:
        return u'wtorek'
    elif weekday == 2:
        return u'środa'
    elif weekday == 3:
        return u'czwartek'
    elif weekday == 4:
        return u'piątek'
    elif weekday == 5:
        return u'sobota'
    elif weekday == 6:
        return u'niedziela'
        
def get_pl_month(date):
    month = date.month
    if month == 1:
        return u'stycznia'
    if month == 2:
        return u'lutego'
    if month == 3:
        return u'marca'
    if month == 4:
        return u'kwietnia'
    if month == 5:
        return u'maja'
    if month == 6:
        return u'czerwca'
    if month == 7:
        return u'lipca'
    if month == 8:
        return u'sierpnia'
    if month == 9:
        return u'września'
    if month == 10:
        return u'października'
    if month == 11:
        return u'listopada'
    if month == 12:
        return u'grudnia'

def is_sunday(date):
    return date.weekday() == 6
    
def get_hour_from_string(hm, as_touple = False):
    hm_splitted = hm.split(':')
    hour = hm_splitted[0]
    minutes = hm_splitted[1]
    
    if as_touple:
        return (hour, minutes)
    else:
        hour = hour if int(hour) >=10 else '0%s' % (hour)
        minutes = minutes if int(minutes) >=10 else '0%s' % (minutes)
        return '%s:%s' % (hour, minutes)
    
def get_hours_from_string(hm):
    return hm and hm.split(':')[0] or 12
    
def get_minutes_from_string(hm):
    return hm and hm.split(':')[1] or 0
