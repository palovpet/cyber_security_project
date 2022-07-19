CREATE TABLE endusers (
    id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	admin INTEGER
);

CREATE TABLE things (
    id SERIAL PRIMARY KEY,
	owner_id INTEGER REFERENCES endusers,
	thing TEXT,
	hits INTEGER
);