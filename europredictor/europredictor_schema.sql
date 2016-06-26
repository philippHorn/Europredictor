-- sqlite3 database.db < europredictor.sql

PRAGMA foreign_keys = ON;

DROP TABLE if exists comments;
CREATE TABLE comments (
  id INTEGER PRIMARY KEY autoincrement,
  thread_url TEXT NOT NULL,
  thread_title TEXT,
  comment_url TEXT NOT NULL,
  'timestamp' TIMESTAMP,
  username TEXT NOT NULL,
  comment TEXT NOT NULL,
  country TEXT NOT NULL,
  pos_sentiment NUMERIC,
  neu_sentiment NUMERIC,
  neg_sentiment NUMERIC,
  comp_sentiment NUMERIC,
  CHECK (
        typeof("pos_sentiment") = "real" AND
        typeof("neu_sentiment") = "real" AND
        typeof("neg_sentiment") = "real" AND
        typeof("comp_sentiment") = "real"
  )
);


