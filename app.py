from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from mysqlite import DBManager

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SPORT = [
    "Basketball",
    "Football",
    "Volleyball"
]
sqldb = DBManager(db_file_path="demo.db")

@app.route("/")
def index():
    return render_template("index.html", SPORT=SPORT)

@app.route("/deregister", methods=["POST"])
def deregister():
    name = request.form.get("dename")
    if name:
        sqldb.execute(f'DELETE FROM reg WHERE name = "{name}";')
    return redirect("/registrants")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORT:
        return render_template("failure.html")
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

if __name__ == "__main__":
    app.run(debug=True)
