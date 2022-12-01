-- user_account definition

CREATE TABLE user_account (
	user_account_id BIGINT NOT NULL,
	name VARCHAR,
	username VARCHAR,
	about VARCHAR,
	categories VARCHAR,
	location VARCHAR,
	website VARCHAR,
	joined_date DATETIME,
	birthdate DATETIME,
	is_verified BOOLEAN,
	is_private BOOLEAN,
	is_official_account BOOLEAN,
	email VARCHAR,
	password VARCHAR,
	phone_number VARCHAR,
	country VARCHAR,
	PRIMARY KEY (user_account_id)
);