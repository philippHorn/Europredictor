-- sqlite3 database.db < europredictor.sql

PRAGMA foreign_keys = ON;

DROP TABLE if exists clauses;
CREATE TABLE clauses (
  id INTEGER PRIMARY KEY autoincrement,
  thread_url TEXT NOT NULL,
  comment_url TEXT NOT NULL,
  'timestamp' TIMESTAMP,
  username TEXT NOT NULL,
  clause TEXT NOT NULL,
  team TEXT NOT NULL,
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

