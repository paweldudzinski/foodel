CREATE TABLE users (
    id bigserial primary key, 
    
    email varchar(100) not null,
    password varchar(100) not null,
    md5 varchar(100) not null,

    name varchar(100) not null,
    company varchar(1000) null,
    street varchar(1000) null,
    zip varchar(6) null,
    city varchar(1000) null,
    country varchar(1000) null,
    vat_id varchar(1000) null,
    lg_id varchar(2) default 'pl',
    is_admin boolean default false,
    confirmed boolean default false
);

CREATE TABLE categories (
    id bigserial primary key, 
    lg_id varchar(2) default 'pl',
    name varchar(2000) not null,
    parent_id int null,
    coupled int[] null,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1, 'pl', 'Nabiał', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (101, 'pl', 'Mleko', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (102, 'pl', 'Jaja', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (103, 'pl', 'Masła', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (104, 'pl', 'Żółte sery', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (105, 'pl', 'Twarde sery', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (106, 'pl', 'Sery podpuszczkowe', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (107, 'pl', 'Twarogi', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (108, 'pl', 'Domowe jogurty', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (109, 'pl', 'Produkty sojowe', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (110, 'pl', 'Lody', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (111, 'pl', 'Shake', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (112, 'pl', 'Bakterie do serów', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (113, 'pl', 'Lokalne produkty', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (114, 'pl', 'Inne produkty mleczne', 1);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (2, 'pl', 'Oleje i tłuszcze', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (201, 'pl', 'Oleje roślinne', 2);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (202, 'pl', 'Oliwy', 2);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (203, 'pl', 'Tłuszcze zwierzęce', 2);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (204, 'pl', 'Masła', 2);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (205, 'pl', 'Ghi', 2);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (206, 'pl', 'Egzotyki', 2);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (3, 'pl', 'Owoce', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (301, 'pl', 'Lokalne', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (302, 'pl', 'Jagody ', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (303, 'pl', 'Owoce leśne', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (304, 'pl', 'Cytrusy', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (305, 'pl', 'Egzotyczne', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (306, 'pl', 'Dżemy ', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (307, 'pl', 'Nasiona', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (308, 'pl', 'Suszone owoce', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (309, 'pl', 'Bakalie', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (310, 'pl', 'Owoce morza', 3);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (4, 'pl', 'Warzywa', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (401, 'pl', 'Lokalne', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (402, 'pl', 'Orientalne', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (403, 'pl', 'Strączkowe', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (404, 'pl', 'Zioła', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (405, 'pl', 'Chutneje', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (406, 'pl', 'Przetwory', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (407, 'pl', 'Nasiona', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (408, 'pl', 'Nietypowe', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (409, 'pl', 'Grzyby', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (410, 'pl', 'Kwiaty', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (411, 'pl', 'Kiełki', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (412, 'pl', 'Pasztety warzywne', 4);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (5, 'pl', 'Słodycze i frykasy', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (501, 'pl', 'Bakalie', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (502, 'pl', 'Ciasta', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (503, 'pl', 'Desery', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (504, 'pl', 'Ciastka', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (505, 'pl', 'Praliny', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (506, 'pl', 'Lody', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (507, 'pl', 'Czekolady', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (508, 'pl', 'Jogurty', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (509, 'pl', 'Dżemy', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (510, 'pl', 'Napoje', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (511, 'pl', 'Orzechy', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (512, 'pl', 'Czekadełka', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (512, 'pl', 'Sorbety', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (513, 'pl', 'Inne', 5);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (6, 'pl', 'Pieczywo ', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (601, 'pl', 'Domowy chleb', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (602, 'pl', 'Drożdżówki', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (603, 'pl', 'Wypieki babci', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (604, 'pl', 'Słodkości', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (605, 'pl', 'Zakwasy', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (606, 'pl', 'Mąki', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (607, 'pl', 'Orientalne', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (608, 'pl', 'Bez glutenu', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (609, 'pl', 'Inne', 6);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (7, 'pl', 'Mięso', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (701, 'pl', 'Wieprzowina', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (702, 'pl', 'Wołowina', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (703, 'pl', 'Drób', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (704, 'pl', 'Podroby', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (705, 'pl', 'Jagnięcina', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (706, 'pl', 'Dziczyzna', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (707, 'pl', 'Kiełbasy', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (708, 'pl', 'Pasztety', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (709, 'pl', 'Wędliny', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (710, 'pl', 'Pieczenie', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (711, 'pl', 'Inne', 7);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (8, 'pl', 'Ryby i owoce morza', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (801, 'pl', 'Ryby ', 8);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (802, 'pl', 'Owoce morza', 8);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (9, 'pl', 'Przyprawy, zioła i grzyby', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (901, 'pl', 'Grzyby', 9);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (902, 'pl', 'świeże zioła', 9);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (903, 'pl', 'Przyprawy', 9);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (904, 'pl', 'Mieszanki przypraw', 9);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (905, 'pl', 'Orientalne', 9);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (906, 'pl', 'Inne', 9);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (10, 'pl', 'Sosy, dipy i pasty', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1001, 'pl', 'Pesta', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1002, 'pl', 'Pasty', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1003, 'pl', 'Chatneye', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1004, 'pl', 'Keczupy', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1005, 'pl', 'Musztardy', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1006, 'pl', 'Majonezy', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1007, 'pl', 'Orientalne', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1008, 'pl', 'Dipy', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1009, 'pl', 'Smarowidła', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1010, 'pl', 'Masła', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1011, 'pl', 'Marynaty', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1012, 'pl', 'Sosy', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1013, 'pl', 'Inne', 10);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (11, 'pl', 'Przetwory', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1101, 'pl', 'Dżemy', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1102, 'pl', 'Chatneye', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1103, 'pl', 'Przetwory', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1104, 'pl', 'Soki', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1105, 'pl', 'Mrożonki', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1106, 'pl', 'Marynaty', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1107, 'pl', 'Pikle', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1108, 'pl', 'Koncentraty', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1109, 'pl', 'Syropy', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1110, 'pl', 'Vegimamite', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1111, 'pl', 'Ghi', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1112, 'pl', 'Mąki', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1113, 'pl', 'Inne', 11);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (12, 'pl', 'Napoje', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1201, 'pl', 'Lemoniady', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1202, 'pl', 'Soki', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1203, 'pl', 'Wody lecznicze', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1204, 'pl', 'Wody', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1205, 'pl', 'Piwa', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1206, 'pl', 'Shake', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1207, 'pl', 'Kwas chlebowy', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1208, 'pl', 'Podpiwek', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1209, 'pl', 'Nalewki', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1210, 'pl', 'Jogurty', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1211, 'pl', 'Czekolady', 12);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (13, 'pl', 'Kawy i herbaty', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1301, 'pl', 'Kawy ', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1302, 'pl', 'Herbaty', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1303, 'pl', 'Mieszkanki ziołowe', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1304, 'pl', 'Yerba', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1305, 'pl', 'Napary', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1306, 'pl', 'Babble tea', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1307, 'pl', 'Cukier', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1308, 'pl', 'Słodziki', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1309, 'pl', 'Przyprawy i dodatki', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1310, 'pl', 'Inne', 13);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (14, 'pl', 'Zboża, makarony, ryż i kasze', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1401, 'pl', 'Makaron', 14);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1402, 'pl', 'Ryż ', 14);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1403, 'pl', 'Kasza', 14);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1404, 'pl', 'Płatki owsiane', 14);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1405, 'pl', 'Mąka', 14);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1406, 'pl', 'Inne', 14);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (15, 'pl', 'Kwiaty', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1501, 'pl', 'Kwiaty jadalne', 15);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1502, 'pl', 'Kwiaty ozdobne', 15);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1503, 'pl', 'Kiełki', 15);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1504, 'pl', 'Inne', 15);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (16, 'pl', 'Dania główne', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1601, 'pl', 'Niskokaloryczne', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1602, 'pl', 'Bez glutenu', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1603, 'pl', 'Bez laktozy', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1604, 'pl', 'Dietetyczne', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1605, 'pl', 'Bez soli', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1606, 'pl', 'Niskotłuszczowe', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1607, 'pl', 'Niski indeks glikemiczny', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1608, 'pl', 'Wegetariańskie', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1609, 'pl', 'Weganskie', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1610, 'pl', 'Z lokalnych produktów', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1611, 'pl', 'Dla dzieci', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1612, 'pl', 'Orientalne', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1613, 'pl', 'Na ostro', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1614, 'pl', 'Na tłusto', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1615, 'pl', 'Mięsne', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1616, 'pl', 'Rybne', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1617, 'pl', 'Desery', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1618, 'pl', 'Zupy', 16);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1619, 'pl', 'Pięć przemian', 16);

CREATE TABLE locations (
    id bigserial primary key, 
    name varchar(200) not null,
    woj_id int null,
    FOREIGN KEY (woj_id) REFERENCES locations(id)
);

CREATE TABLE products (
    id bigserial primary key, 
    name varchar(1000) null,
    kind varchar(1) not null,         
    state varchar(1) not null default 'A',
    localisation varchar(1000) null,
    bargain_type varchar(1) not null,   
    bargain_type_freetext TEXT,
    price DECIMAL(20,2) null, 
    shipping_price DECIMAL(20,2) null,
    availability varchar(1) not null,
    shipping_method varchar(1) not null,
    shipping_method_freetext TEXT,
    quantity int null,
    quantity_measure varchar(1) null,
    end_date timestamp null,
    
    rating_count int null,
    rating_sum int null,
    
    description TEXT,
    
    mlang varchar(100) null,
    mlong varchar(100) null,
    
    us_id int not null,
    cat_id int not null,
    subcat_id int not null,
    subcat2_id int null,
    loc_id int null,
    specifics int[] null,
    FOREIGN KEY (us_id) REFERENCES users(id),
    FOREIGN KEY (cat_id) REFERENCES categories(id),
    FOREIGN KEY (subcat_id) REFERENCES categories(id),
    FOREIGN KEY (subcat2_id) REFERENCES categories(id),
    FOREIGN KEY (loc_id) REFERENCES locations(id)
    
);

CREATE TABLE events (
    id bigserial primary key,
    us_id int not null,
    when_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event_starts timestamp NULL,
    event_ends timestamp NULL,
    title varchar(1000) NOT NULL,
    description varchar(8000) NULL,
    facebook_url varchar(1000) null,
    
    mlang varchar(100) null,
    mlong varchar(100) null,
    localisation varchar(1000) null,
    loc_id int null,
    FOREIGN KEY (loc_id) REFERENCES locations(id),
    FOREIGN KEY (us_id) REFERENCES users(id)
);

CREATE TABLE photos (
    id bigserial primary key, 
    filepath varchar(2000) not null,
    is_main boolean default false,
    product_id int null,
    us_id int null,
    event_id int null,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (us_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE threads (
    id bigserial primary key, 
    when_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    when_updated timestamp NOT NULL,
    from_us_id int not null,
    to_us_id int not null,
    product_id int not null,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (from_us_id) REFERENCES users(id),
    FOREIGN KEY (to_us_id) REFERENCES users(id)
);

CREATE TABLE messages (
    id bigserial primary key, 
    when_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    thread_id int not null,
    from_us_id int not null,
    to_us_id int not null,
    direction varchar(2) not null,
    read boolean default false,
    message TEXT,
    FOREIGN KEY (from_us_id) REFERENCES users(id),
    FOREIGN KEY (to_us_id) REFERENCES users(id),
    FOREIGN KEY (thread_id) REFERENCES threads(id)
);

CREATE TABLE orders (
    id bigserial primary key, 
    when_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    seller_us_id int not null,
    buyer_us_id int not null,
    product_id int not null,
    thread_id int not null,
    buyer_status varchar(1) not null default 'N',
    seller_status varchar(1) not null default 'N',
    quantity int not null,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (seller_us_id) REFERENCES users(id),
    FOREIGN KEY (buyer_us_id) REFERENCES users(id),
    FOREIGN KEY (thread_id) REFERENCES threads(id)
);

CREATE TABLE votes (
    id bigserial primary key, 
    hat_count int not null,
    us_id int not null,
    product_id int not null,
    FOREIGN KEY (us_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE specifics (
    id bigserial primary key, 
    name varchar(100) not null
);

INSERT INTO specifics (id, name) VALUES (1, 'Bez laktozy');
INSERT INTO specifics (id, name) VALUES (2, 'Bez glutenu');
INSERT INTO specifics (id, name) VALUES (3, 'Niskokaloryczne');
INSERT INTO specifics (id, name) VALUES (4, 'Wegetariańskie');
INSERT INTO specifics (id, name) VALUES (5, 'Z lokalnych produktów');
INSERT INTO specifics (id, name) VALUES (6, 'Na ostro');
INSERT INTO specifics (id, name) VALUES (7, 'Mięsne');
INSERT INTO specifics (id, name) VALUES (8, 'Rybne');

CREATE TABLE comments (
    id bigserial primary key, 
    comment varchar(5000) not null,
    product_id int not null,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE leads (
    id bigserial primary key, 
    name varchar(200) null,
    email varchar(200) null,
    phone varchar(200) null,
    category varchar(1) default 'P',
    description varchar(5000) null
);

CREATE TABLE email_queue (
    id bigserial primary key, 
    us_id int not null,
    when_sent varchar(200) null,
    type varchar(2) not null,
    email_to varchar(200) not null,
    subject varchar(500) null,
    body varchar(5000) null,
    FOREIGN KEY (us_id) REFERENCES users(id)
);
