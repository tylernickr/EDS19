DROP database if exists github;

CREATE database github;

USE github;

DROP TABLE IF EXISTS github_user;

CREATE TABLE github_user
(
	username	varchar(80)		PRIMARY KEY,
    email		varchar(120) 	NOT NULL
);

DROP TABLE IF EXISTS project;

CREATE TABLE project
(
	id			varchar(255)	PRIMARY KEY,
    name		varchar(120) 	NOT NULL
);

DROP TABLE IF EXISTS commit;

CREATE table commit
(
	hash			char(40)		PRIMARY KEY,
    subject			varchar(255)	NOT NULL,
    message			varchar(2058)	NULL,
    projectID		varchar(255)	NOT NULL,
    author			varchar(80)		NOT NULL,
    authorTime		datetime		NOT NULL,
    committer		varchar(80)		NOT NULL,
    commitTime		datetime		NOT NULL,
    FOREIGN KEY project_key(projectID) REFERENCES project(id),
    FOREIGN KEY author_key(author) REFERENCES github_user(username),
    FOREIGN KEY committer_key(committer) REFERENCES github_user(username)
);