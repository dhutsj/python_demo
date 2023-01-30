from flask import Flask, render_template, request

app = Flask(__name__)

reg = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    reg[name] = sport
    return render_template("success.html")

@app.route("/registrants")
def registrants():
    return render_template("registrants.html", reg=reg)

if __name__ == "__main__":
    app.run(debug=True)
