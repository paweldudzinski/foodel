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


DELETE FROM categories;
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (1, 'pl', 'Jedzenie', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (2, 'pl', 'Pieczywo', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (3, 'pl', 'Mięso', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (4, 'pl', 'Przetwory', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (5, 'pl', 'Pasty i sosy', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (6, 'pl', 'Przyprawy, zioła i grzyby', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (7, 'pl', 'Słodkości', null);
INSERT INTO categories (id, lg_id, name, parent_id) VALUES (8, 'pl', 'Piwo i', null);



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
    when_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comment varchar(5000) not null,
    product_id int not null,
    us_id int not null,
    FOREIGN KEY (us_id) REFERENCES users(id),
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
