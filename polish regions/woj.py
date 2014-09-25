# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import json
xml = open('TERC.xml', 'r')
soup = BeautifulSoup(xml)

poland = {}

for row in soup.findAll('row'):
    woj_id = pow_id = gmi_id = nazwa = None
    for col in row.findAll('col'):
        if col['name'] == 'WOJ':
            woj_id = col.next
        if col['name'] == 'NAZWA':
            nazwa = col.next
        if col['name'] == 'NAZDOD':
            nazdod = col.next
            
    if nazdod == u'województwo':
        poland[int(woj_id)] = {
            'nazwa' : nazwa.capitalize(),
            'miasta' : []
        }
        
for row in soup.findAll('row'):
    woj_id = pow_id = gmi_id = nazwa = None
    for col in row.findAll('col'):
        if col['name'] == 'WOJ':
            woj_id = col.next
        if col['name'] == 'GMI':
            gmi_id = col.next
        if col['name'] == 'NAZWA':
            nazwa = col.next
        if col['name'] == 'NAZDOD':
            nazdod = col.next

    if nazdod[:6] == u'miasto':
        poland[int(woj_id)]['miasta'].append(nazwa)
    
    
        
for id, data in poland.iteritems():
    sql = 'INSERT INTO locations (id, woj_id, name) VALUES (%d, null, "%s");' % (id, data['nazwa'])
    print sql
for id, data in poland.iteritems():
    for i, miasto in enumerate(data['miasta']):
        sql = 'INSERT INTO locations (id, woj_id, name) VALUES (%d, %d, "%s");' % (int("%s%s"%(id,i+100)), id, miasto)
        print sql
