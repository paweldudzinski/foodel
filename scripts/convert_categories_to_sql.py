# -*- coding: utf-8 -*-
categories="""nabiał
mleko
jaja
masła
żółte sery
twarde sery
sery podpuszczkowe
twarogi
domowe jogurty
produkty sojowe
lody
shake
bakterie do serów
lokalne produkty
inne produkty mleczne
*
oleje i tłuszcze
oleje roślinne
oliwy
tłuszcze zwierzęce
masła
ghi
egzotyki
*
owoce
lokalne
jagody 
owoce leśne
cytrusy
egzotyczne
dżemy 
nasiona
suszone owoce
bakalie
owoce morza
*
warzywa
lokalne
orientalne
strączkowe
zioła
chutneje
przetwory
nasiona
nietypowe
grzyby
kwiaty
kiełki
pasztety warzywne
*
słodycze i frykasy
bakalie
ciasta
desery
ciastka
praliny
lody
czekolady
jogurty
dżemy
napoje
orzechy
czekadełka
inne
*
pieczywo 
domowy chleb
drożdżówki
wypieki babci
słodkości
zakwasy
mąki
orientalne
bez glutenu
inne
*
mięso
wieprzowina
wołowina
drób
podroby
jagnięcina
dziczyzna
kiełbasy
pasztety
wędliny
pieczenie
inne
*
ryby i owoce morza
ryby 
owoce morza
*
przyprawy, zioła i grzyby
grzyby
świeże zioła
przyprawy
mieszanki przypraw
orientalne
inne
*
sosy, dipy i pasty
pesta
pasty
chatneye
keczupy
musztardy
majonezy
orientalne
dipy
smarowidła
masła
marynaty
sosy
inne
*
przetwory
dżemy
chatneye
przetwory
soki
mrożonki
marynaty
pikle
koncentraty
syropy
vegimamite
ghi
mąki
inne
*
napoje
lemoniady
soki
wody lecznicze
wody
piwa
shake
kwas chlebowy
podpiwek
nalewki
jogurty 
*
kawy i herbaty
kawy 
herbaty
mieszkanki ziołowe
yerba
napary
babble tea
cukier
słodziki
przyprawy i dodatki
inne
*
zboża, makarony, ryż i kasze
makaron
ryż 
kasza
płatki owsiane
mąka
inne
*
kwiaty
kwiaty jadalne
kwiaty ozdobne
kiełki
inne"""
w = open("../kj/database/categories.sql", "w")
for j, c in enumerate(categories.split('*')):
    for i, k in enumerate(c.strip().split('\n')):
        index = j+1
        if i < 10:
            subindex = int("%s0%s"%(index,i))
        else:
            subindex = int("%s%s"%(index,i))
        if not i:
            line = "INSERT INTO categories (id, lg_id, name, parent_id) VALUES (%d, 'pl', '%s', null);\n" % (index, k.capitalize())
        else:
            line = "INSERT INTO categories (id, lg_id, name, parent_id) VALUES (%s, 'pl', '%s', %d);\n" % (subindex, k.capitalize(), index)
            
        w.writelines(line)
            
    
    












