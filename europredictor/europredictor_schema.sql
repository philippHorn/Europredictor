-- sqlite3 database.db < europredictor.sql

PRAGMA foreign_keys = ON;

DROP TABLE if exists countries;
CREATE TABLE countries (
  id INTEGER PRIMARY KEY autoincrement,
  name TEXT NOT NULL
);

DROP TABLE if exists comments;
CREATE TABLE comments (
  id INTEGER PRIMARY KEY autoincrement,
  'timestamp' TIMESTAMP,
  comment TEXT NOT NULL,
  flair TEXT,
  score INTEGER,
  country INTEGER NOT NULL,
  pos_sentiment NUMERIC,
  neg_sentiment NUMERIC,
  FOREIGN KEY(country) REFERENCES countries(id)
  CHECK (
        typeof("pos_sentiment") = "real" AND
        typeof("neg_sentiment") = "real"
  )
);



