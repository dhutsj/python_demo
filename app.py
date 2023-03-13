from flask import Flask, render_template, request, redirect, session
# from flask_session import Session

import time
from mysqlite import DBManager

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from prometheus_client import start_http_server
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "demoapp"
})

# Start Prometheus client
start_http_server(port=8000, addr="0.0.0.0")
# Initialize PrometheusMetricReader which pulls metrics from the SDK
# on-demand to respond to scrape requests
reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)


resource = Resource(attributes={
    SERVICE_NAME: "demoapp"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="0.0.0.0",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)

meter = metrics.get_meter(__name__)

# Now create a counter instrument to make measurements with
app_counter = meter.create_counter(
    "app_counter",
    description="The total visited number of this app",
)

app = Flask(__name__)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

SPORT = [
    "Basketball",
    "Football",
    "Volleyball"
]
sqldb = DBManager(db_file_path="demo.db")

@app.route("/")
def index():
    with tracer.start_as_current_span("index") as span:
        span.set_attribute("page.location", "index")
        app_counter.add(1, {"page.location": "index"})
        return render_template("index.html", SPORT=SPORT)

@app.route("/deregister", methods=["POST"])
def deregister():
    name = request.form.get("dename")
    if name:
        sqldb.execute(f'DELETE FROM reg WHERE name = "{name}";')
    return redirect("/registrants")

@app.route("/register", methods=["POST"])
def register():
    # hello_demo()
    with tracer.start_as_current_span("register") as span:
        span.set_attribute("page.location", "register")
        name = request.form.get("name")
        sport = request.form.get("sport")
        if not name or sport not in SPORT:
            return render_template("failure.html")
        span.set_attribute("registered.user", name)
        reg = sqldb.execute(f'SELECT * FROM reg WHERE name = "{name}";')
        if reg:
            sqldb.execute(f'UPDATE reg SET sport = "{sport}" WHERE name = "{name}";')
            return redirect("/registrants")
        sqldb.execute(f'INSERT INTO reg (name, sport) VALUES("{name}", "{sport}");')
        return redirect("/registrants")

@app.route("/registrants")
def registrants():
    reg = sqldb.execute("SELECT * FROM reg;")
    return render_template("registrants.html", reg=reg)

def hello_demo():
        time.sleep(1)
        print("hello demo")


if __name__ == "__main__":
    app.run(debug=True)
