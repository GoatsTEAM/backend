CREATE TYPE role_enum AS ENUM ('admin', 'buyer', 'seller', 'operator');
CREATE TYPE gender_enum AS ENUM ('male', 'female');

CREATE TABLE users_credentials (
    user_id       SERIAL PRIMARY KEY,
    email         VARCHAR   NOT NULL UNIQUE,
    hash_password VARCHAR   NOT NULL,
    is_banned     BOOLEAN   NOT NULL DEFAULT FALSE,
    role          role_enum NOT NULL
);

CREATE TABLE users_profile (
    user_id         INTEGER REFERENCES users_credentials (user_id) PRIMARY KEY,
    first_name      VARCHAR                 NOT NULL,
    last_name       VARCHAR                 NOT NULL,
    gender          gender_enum,
    phone           VARCHAR,
    avatar          VARCHAR,
    created_at      TIMESTAMP DEFAULT now() NOT NULL,

    passport_number VARCHAR,
    birth_date      DATE,
    tax_id          VARCHAR
);