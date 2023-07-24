from flask import Flask, render_template, request, session, redirect, flash, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from cs50 import SQL
from helpers import apology, login_required

app = Flask(__name__)

#auto-reloaded templates
app.config["TEMPALTES_AUTO_RELOAD"] = True

#Store the session data on the server instead in the user's computer
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

@app.after_request #TIRAR SE NAO SERVIR DE NADA
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    user_id = session["user_id"]

    if request.method == "GET":
        pet_list = db.execute("SELECT id, petname, petage, petbreed FROM pets WHERE user_id = ?", user_id)
        return render_template("index.html", pet_list=pet_list)
        #return jsonify(pet_list)
    else:
        remove_pet = request.form.get("remove_pet")
        #return jsonify(remove_pet)

        if remove_pet:
            db.execute("DELETE FROM pets WHERE id = ?", remove_pet)
            return redirect("/")




@app.route("/petmenu", methods=["GET", "POST"])
@login_required
def petmenu():

    user_id = session["user_id"]
    pet_id = db.execute("SELECT id FROM pets WHERE user_id = ?", user_id)

    if request.method == "POST":
        id_acaricide = request.form.get("id_acaricide")
        id_vaccine = request.form.get("id_vaccine")
        id_vermifuge = request.form.get("id_vermifuge")

        if id_acaricide:
            db.execute("DELETE FROM acaricides WHERE id = ?", id_acaricide)
            return redirect("petmenu")
        if id_vaccine:
            db.execute("DELETE FROM vaccines WHERE id = ?", id_vaccine)
            return redirect("petmenu")
        if id_vermifuge:
            db.execute("DELETE FROM vermifuges WHERE id = ?", id_vermifuge)
            return redirect("petmenu")


    else:
        #return jsonify(pet_id)

        vaccine_list = db.execute("SELECT * FROM vaccines WHERE user_id = ?", user_id)
        acaricide_list = db.execute("SELECT * FROM acaricides WHERE user_id = ?", user_id)
        vermifuge_list = db.execute("SELECT * FROM vermifuges WHERE user_id = ?", user_id)
        return render_template("petmenu.html", vaccine_list=vaccine_list, acaricide_list=acaricide_list, vermifuge_list=vermifuge_list)


@app.route("/registeracaricide", methods=["GET", "POST"])
@login_required
def registeracaricide():

    user_id = session["user_id"]

    if request.method == "POST":

        acaricide_name = request.form["acaricidename"]
        acaricide_date = request.form["acaricidedate"]
        pet = request.form["petname"]

        if not acaricide_name:
            return apology("Must provide an Acaricide Name", 400)
        elif not acaricide_date:
            return apology("Must provide a Acaricide Date", 400)
        elif not pet:
            return apology("Must Provide a Pet", 400)

        pet_id = db.execute("SELECT id FROM pets WHERE petname = ?", pet)


        db.execute("INSERT INTO acaricides (user_id, pet_id, name, acaricidename, nextacaricide) VALUES (?, ?, ?, ?, ?)", user_id, pet_id[0]['id'], pet, acaricide_name, acaricide_date)

        flash('Next Acaricide scheduled!')
        return redirect("petmenu")

    else:
        pet_name = db.execute("SELECT petname FROM pets WHERE user_id = ?", user_id)


        return render_template("registeracaricide.html", pet_name=pet_name)


@app.route("/registervaccine", methods=["GET", "POST"])
@login_required
def registervaccine():

    user_id = session["user_id"]

    if request.method == "POST":

        vaccine_name = request.form["vaccinename"]
        vaccine_date = request.form["vaccinedate"]
        pet = request.form["petname"]

        if not vaccine_name:
            return apology("Must provide Vaccine Name", 400)
        elif not vaccine_date:
            return apology("Must provide a Vaccine Date", 400)
        elif not pet:
            return apology("Must Provide a Pet", 400)

        pet_id = db.execute("SELECT id FROM pets WHERE petname = ?", pet)


        db.execute("INSERT INTO vaccines (user_id, pet_id, vaccinename, nextvaccine, name) VALUES (?, ?, ?, ?, ?)", user_id, pet_id[0]['id'], vaccine_name, vaccine_date, pet)

        flash('Next Vaccine scheduled!')
        return redirect("petmenu")

    else:
        pet_name = db.execute("SELECT petname FROM pets WHERE user_id = ?", user_id)


        return render_template("registervaccine.html", pet_name=pet_name)


@app.route("/registervermifuge", methods=["GET", "POST"])
@login_required
def registervermifuge():

    user_id = session["user_id"]

    if request.method == "POST":

        vermifuge_name = request.form["vermifugename"]
        vermifuge_date = request.form["vermifugedate"]
        pet = request.form["petname"]

        if not vermifuge_name:
            return apology("Must provide a Vermifuge Name", 400)
        elif not vermifuge_date:
            return apology("Must provide a Varmifuge Date", 400)
        elif not pet:
            return apology("Must Provide a Pet", 400)

        pet_id = db.execute("SELECT id FROM pets WHERE petname = ?", pet)


        db.execute("INSERT INTO vermifuges (user_id, pet_id, vermifugename, nextvermifuge, name) VALUES (?, ?, ?, ?, ?)", user_id, pet_id[0]['id'], vermifuge_name, vermifuge_date, pet)

        flash('Next Vermifuge scheduled!')
        return redirect("petmenu")

    else:
        pet_name = db.execute("SELECT petname FROM pets WHERE user_id = ?", user_id)


        return render_template("registervermifuge.html", pet_name=pet_name)


@app.route("/registerpet", methods=["GET", "POST"])
@login_required
def registerpet():

    user_id = session["user_id"]

    if request.method == "GET":
        return render_template("registerpet.html")

    else:
        petname = request.form["petname"]
        petage = request.form["petage"]
        petbreed = request.form["petbreed"]

        if not petname:
            return apology("Must provide a Pet Name", 400)
        elif not petage:
            return apology("Must provide a Pet Age", 400)
        elif not petbreed:
            return apology("Must Provide a Breed", 400)

        db.execute("INSERT INTO pets (user_id, petname, petage, petbreed) VALUES (?, ?, ?, ?)", user_id, petname, petage, petbreed)

        flash('Registration completed!')

        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirmation = request.form['confirmation']
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username:
            return apology("Must provide an username", 400)

        elif rows:
            return apology("Username already exists")

        elif not password:
            return apology("Must provide a password", 400)

        elif password != confirmation:
            return apology("Passwords do not match", 400)

        pass_hash = generate_password_hash(password)
        new_user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, pass_hash)

        session["user_id"] = new_user

        flash('Registration completed!')

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")
