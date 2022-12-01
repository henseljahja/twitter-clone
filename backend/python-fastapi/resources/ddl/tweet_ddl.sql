-- tweet definition

CREATE TABLE tweet (
	tweet_id BIGINT NOT NULL,
	text VARCHAR,
	source VARCHAR,
	created_date DATETIME,
	user_account_id BIGINT,
	PRIMARY KEY (tweet_id),
	FOREIGN KEY(user_account_id) REFERENCES user_account (user_account_id)
);