CREATE TABLE users (
    id INTEGER PRIMARY KEY, 
    username TEXT UNIQUE, 
    password_hash TEXT
);

CREATE TABLE companies (
    id INTEGER PRIMARY KEY, 
    name TEXT UNIQUE, 
    stock_amount INTEGER, 
    last_price INTEGER, owner TEXT, 
    industry TEXT
);

CREATE TABLE portfolios (
    id INTEGER PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    company_id INTEGER REFERENCES 
    companies, 
    amount INTEGER
);