from flask import Flask, render_template, request, redirect
from mysqlite import DBManager

app = Flask(__name__)

SPORT = [
    "Basketball",
    "Football",
    "Volleyball"
]
sqldb = DBManager(db_file_path="demo.db")

@app.route("/")
def index():
    return render_template("index.html", SPORT=SPORT)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORT:
        return render_template("failure.html")
    sqldb.execute(f'INSERT INTO reg (name, sport) VALUES("{name}", "{sport}");')
    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    reg = sqldb.execute("SELECT * FROM reg;")
    return render_template("registrants.html", reg=reg)

if __name__ == "__main__":
    app.run(debug=True)
