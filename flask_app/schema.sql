DROP TABLE if EXISTS maps; /* Reset database on creation */
CREATE TABLE maps (
  id integer PRIMARY KEY AUTOINCREMENT,
  file_reference text NOT NULL /* reference to location in filesystem */
);
CREATE TABLE meetings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  time TEXT NOT NULL, /* YYYY-MM-DD HH:MM:SS.SSS */
  map_id INTEGER NOT NULL,
  FOREIGN KEY(map_id) REFERENCES maps(id)
);
INSERT INTO maps (file_reference) VALUES ('maps/mymap');
INSERT INTO meetings (time, map_id) VALUES ('1992-12-18 15:10:20.101', 1);