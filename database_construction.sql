CREATE TABLE UserData (
username VARCHAR(20) NOT NULL,
hash VARCHAR(200) NOT NULL,
token VARCHAR(50) NOT NULL,
invite_code VARCHAR(10) NOT NULL,
was_invited_with VARCHAR(10) NOT NULL,
money FLOAT NOT NULL,
PRIMARY KEY(username)
);

CREATE UNIQUE INDEX ind_token
ON UserData (token);

CREATE UNIQUE INDEX ind_invite_code
ON UserData (invite_code);

CREATE INDEX ind_hash
ON UserData (hash);
