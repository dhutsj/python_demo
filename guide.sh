#! /bin/bash

sqlite3 demo.db

CREATE TABLE reg (name TEXT NOT NULL, sport TEXT NOT NULL);
.schema

INSERT INTO reg (name, sport) VALUES("TSJ", "Basketball");
SELECT * FROM reg;
