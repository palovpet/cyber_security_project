CREATE TABLE endusers (
    id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT
);


CREATE TABLE things (
    id SERIAL PRIMARY KEY,
	owner_id INTEGER REFERENCES endusers,
	thing TEXT
);