#! /bin/bash

sqlite3 demo.db

CREATE TABLE reg (name TEXT NOT NULL, sport TEXT NOT NULL);
.schema

INSERT INTO reg (name, sport) VALUES("TSJ", "Basketball");
SELECT * FROM reg;
UPDATE reg SET sport = "Football" WHERE name = "TSJ";
DELETE FROM reg WHERE name = "TSJ";

# https://opentelemetry.io/docs/instrumentation/python/exporters/
flask run
opentelemetry-instrument --traces_exporter console --metrics_exporter console flask run
opentelemetry-instrument flask run
# http://localhost:16686 jaeger
