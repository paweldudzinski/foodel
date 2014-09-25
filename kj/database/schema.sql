CREATE TABLE users (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    
    email varchar(100) not null,
    password varchar(100) not null,

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
) engine = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE categories (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    lg_id varchar(2) default 'pl',
    name varchar(2000) not null,
    parent_id int null,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
) engine = InnoDB DEFAULT CHARSET=utf8;

INSERT INTO categories SET id=0, lg_id = 'pl', name='Lekcje gotowania', parent_id = null;
INSERT INTO categories SET id=1, lg_id = 'pl', name='Potrawy', parent_id = null;
INSERT INTO categories SET id=2, lg_id = 'pl', name='Bakalie', parent_id = null;
INSERT INTO categories SET id=3, lg_id = 'pl', name='Desery', parent_id = null;
INSERT INTO categories SET id=4, lg_id = 'pl', name='Mięsa', parent_id = null;
INSERT INTO categories SET id=5, lg_id = 'pl', name='Miody', parent_id = null;
INSERT INTO categories SET id=6, lg_id = 'pl', name='Świerze warzywa', parent_id = null;
INSERT INTO categories SET id=7, lg_id = 'pl', name='Świerze owoce', parent_id = null;
INSERT INTO categories SET id=8, lg_id = 'pl', name='Napoje', parent_id = null;
INSERT INTO categories SET id=9, lg_id = 'pl', name='Owoce morza', parent_id = null;
INSERT INTO categories SET id=10, lg_id = 'pl', name='Pasty i sosy', parent_id = null;
INSERT INTO categories SET id=11, lg_id = 'pl', name='Produkty mleczarkie', parent_id = null;
INSERT INTO categories SET id=12, lg_id = 'pl', name='Produkty zbożowe', parent_id = null;
INSERT INTO categories SET id=13, lg_id = 'pl', name='Przekąski', parent_id = null;
INSERT INTO categories SET id=14, lg_id = 'pl', name='Przetwory', parent_id = null;
INSERT INTO categories SET id=15, lg_id = 'pl', name='Przyprawy', parent_id = null;
INSERT INTO categories SET id=16, lg_id = 'pl', name='Tłuszcze jadalne', parent_id = null;
INSERT INTO categories SET id=17, lg_id = 'pl', name='Wędliny', parent_id = null;


CREATE TABLE products (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    name varchar(1000) null,
    kind varchar(1) not null,           /* (S)przedam, (G)otuje, (U)cze */
    state varchar(1) not null default 'A',
    localisation varchar(1000) null,
    bargain_type varchar(1) not null,   /* (S)przedam, (W)ymiana, (I)nne */ 
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
    
    us_id int not null,
    cat_id int not null,
    FOREIGN KEY (us_id) REFERENCES users(id),
    FOREIGN KEY (cat_id) REFERENCES categories(id)
    
) engine = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE photos (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    filepath varchar(2000) not null,
    is_main boolean default false,
    product_id int null,
    us_id int null,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (us_id) REFERENCES users(id)
) engine = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE threads (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    when_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    when_updated timestamp NOT NULL,
    from_us_id int not null,
    to_us_id int not null,
    product_id int not null,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (from_us_id) REFERENCES users(id),
    FOREIGN KEY (to_us_id) REFERENCES users(id)
) engine = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE messages (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    when_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    thread_id int not null,
    from_us_id int not null,
    to_us_id int not null,
    direction varchar(2) not null,
    `read` boolean default false,
    message TEXT,
    FOREIGN KEY (from_us_id) REFERENCES users(id),
    FOREIGN KEY (to_us_id) REFERENCES users(id),
    FOREIGN KEY (thread_id) REFERENCES threads(id)
) engine = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE orders (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    when_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    seller_us_id int not null,
    buyer_us_id int not null,
    product_id int not null,
    thread_id int not null,
    status varchar(1) not null default 'N',
    quantity int not null,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (seller_us_id) REFERENCES users(id),
    FOREIGN KEY (buyer_us_id) REFERENCES users(id),
    FOREIGN KEY (thread_id) REFERENCES threads(id)
) engine = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE votes (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    hat_count int not null,
    us_id int not null,
    product_id int not null,
    FOREIGN KEY (us_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
) engine = InnoDB DEFAULT CHARSET=utf8;



