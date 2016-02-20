DROP TABLE if EXISTS maps; /* Reset database on creation */
CREATE TABLE maps (
  id integer PRIMARY KEY AUTOINCREMENT,
  file_reference text NOT NULL /* reference to location in filesystem */
);
DROP TABLE if EXISTS meetings;
CREATE TABLE meetings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  time TEXT NOT NULL, /* YYYY-MM-DD HH:MM:SS.SSS */
  creator TEXT NOT NULL,
  map_id INTEGER,
  FOREIGN KEY(creator) REFERENCES users(username),
  FOREIGN KEY(map_id) REFERENCES maps(id)
);
DROP TABLE if EXISTS users;
CREATE TABLE users (
  username TEXT PRIMARY KEY,
  password TEXT NOT NULL
);

INSERT INTO maps (file_reference) VALUES ('maps/mymap');
INSERT INTO users (username, password) VALUES ('kari', 'passord');
INSERT INTO meetings (title, time, creator, map_id) VALUES ('Kodeklubb-møte', '1992-12-18 15:10:20.101', 'kari', 1);
INSERT INTO meetings (title, time, creator, map_id) VALUES ('Kløfta møte', '2000-12-18 15:10:20.101', 'kari', 1);