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

#signoz
# https://signoz.io/docs/instrumentation/flask/
OTEL_RESOURCE_ATTRIBUTES=service.name=demoapp OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"  opentelemetry-instrument --traces_exporter otlp_proto_http --metrics_exporter otlp_proto_http flask run
