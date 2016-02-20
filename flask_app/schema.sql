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
  map_id INTEGER,
  FOREIGN KEY(map_id) REFERENCES maps(id)
);
INSERT INTO maps (file_reference) VALUES ('maps/mymap');
INSERT INTO meetings (title, time, map_id) VALUES ('Kodeklubb-møte', '1992-12-18 15:10:20.101', 1);
INSERT INTO meetings (title, time, map_id) VALUES ('Kløfta møte', '2000-12-18 15:10:20.101', 1);