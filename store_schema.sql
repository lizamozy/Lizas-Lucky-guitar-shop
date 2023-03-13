PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  username        varchar(50) not null PRIMARY KEY,
  password        varchar(50) not null,
  email           varchar(50) not null
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
  prod_id         integer not null PRIMARY KEY AUTOINCREMENT,
  prod_name       varchar(50) not null,
  prod_color      varchar(10) not null,
  price           DECIMAL(10,2) not null,
  category        varchar(50) not null,
  stock           int(5)
  
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id        INTEGER not null PRIMARY KEY AUTOINCREMENT,
  user_id         Varchar(50) not null,
  cost            int(1000) not null,
  purch_date      DATETIME not null DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) references users(username) 
  
);

PRAGMA foreign_keys=ON;
-- users
INSERT INTO users VALUES ('testuser', 'testpass', 'testuser@gmail.com');
INSERT INTO users VALUES ('lizamozy', 'HelloHello!@', 'lizamozolyuk@gw.com');

--keys

--products
INSERT INTO products (prod_name, prod_color, price, category, stock) VALUES ('Gibson Les Paul', 'Unburst','2799.99', 'Electric Guitars', '1' );
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Gibson Les Paul', 'Bourbon burst','2799.99', 'Electric Guitars', '2');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Fender Stratocaster', 'Dark Night', '1699.99', 'Electric Guitars', '2');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Yamaha FS830', 'Natural', '339.99', 'Acoustic Guitars', '3');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES ('Yamaha FS830', 'Black', '339.99', 'Acoustic Guitars', '2');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Marshall MG30GFX', 'Black', '499.99', 'Amplifiers', '4');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Orange Super Crush', 'Orange', '699.99', 'Amplifiers', '3');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Orange Super Crush', 'Black', '699.99', 'Amplifiers', '1');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Epiphone Hardshell', 'Black', '129.00', 'Guitar Cases', '5');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Fender Amplifier Cable', 'Black', '15.99', 'Acessories', '10');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Dunlop Guitar Picks', 'Assorted Colors', '6.99', 'Acessories','20');
INSERT INTO products (prod_name,prod_color, price, category, stock) VALUES('Dunlop JH04 Jimi Hendrix Guitar Strap', 'Assorted Colors', '29.99', 'Acessories', '2');
