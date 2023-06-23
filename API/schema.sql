DROP TABLE IF EXISTS "users" CASCADE;

CREATE TABLE "users"(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    useremail TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    token TEXT UNIQUE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS "allow_to";

CREATE TABLE "allow_to"(
    id SERIAL PRIMARY KEY,
    temp_hum BOOLEAN DEFAULT FALSE,
    volt_int BOOLEAN DEFAULT FALSE,
    smoke BOOLEAN DEFAULT FALSE,
    token TEXT UNIQUE NOT NULL,
    CONSTRAINT fk_user
      FOREIGN KEY(token) 
	  REFERENCES "users"(token)
);

DROP TABLE IF EXISTS "max_values";

CREATE TABLE "max_values"(
    id SERIAL PRIMARY KEY,
    temp_max FLOAT DEFAULT 0,
    hum_max FLOAT DEFAULT 0,
    volt_max FLOAT DEFAULT 0,
    int_max FLOAT DEFAULT 0,
    smoke_max FLOAT DEFAULT 0,
    token TEXT UNIQUE NOT NULL,
    CONSTRAINT fk_user
      FOREIGN KEY(token) 
	  REFERENCES "users"(token)
);