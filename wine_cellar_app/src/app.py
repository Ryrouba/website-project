##############################################################################################
##############################################################################################
from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename
import random
from notifypy import Notify

##############################################################################################
##############################################################################################
app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'


app.config['MYSQL_HOST'] = '0.0.0.0'  # Adresse IP de votre serveur MySQL
app.config['MYSQL_PORT'] = 3306  # Port du serveur MySQL
app.config['MYSQL_USER'] = 'root'  # Nom d'utilisateur MySQL
app.config['MYSQL_PASSWORD'] = 'Ryanbaba73'  # Mot de passe MySQL
app.config['MYSQL_DB'] = 'website_projet'  # Nom de la base de données MySQL

##############################################################################################
##############################################################################################
@app.route("/")
def main():
    return render_template('signup.html', template_folder='templates')

##############################################################################################
##############################################################################################
@app.route("/signup", methods=["GET"])
def signup_form():
    return render_template('signup.html')

##############################################################################################
##############################################################################################
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    db_connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

    cursor = db_connection.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user:
        return "Ce nom d'utilisateur est déjà utilisé. Veuillez en choisir un autre."

    insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    user_data = (username, password)
    cursor.execute(insert_query, user_data)

    db_connection.commit()
    cursor.close()
    db_connection.close()

    return redirect("/accueil")

##############################################################################################
##############################################################################################
@app.route("/accueil")
def accueil():
    if 'username' in session:
        username = session['username']

        db_connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        cursor = db_connection.cursor()

        query = "SELECT COUNT(*) FROM shelves INNER JOIN caves ON shelves.cave_id = caves.cave_id WHERE caves.user_id = %s"
        cursor.execute(query, (session['user_id'],))
        num_shelves = cursor.fetchone()[0]

        query = "SELECT COUNT(*) FROM bottles INNER JOIN shelves ON bottles.shelf_id = shelves.shelf_id INNER JOIN caves ON shelves.cave_id = caves.cave_id WHERE caves.user_id = %s"
        cursor.execute(query, (session['user_id'],))
        bottles_count = cursor.fetchone()[0]

        query = "SELECT COUNT(*) FROM caves WHERE user_id = %s"  # Nouvelle requête pour compter le nombre de caves
        cursor.execute(query, (session['user_id'],))
        num_caves = cursor.fetchone()[0]

        user_info = {
            'username': username,
            'num_shelves': num_shelves,
            'bottles_count': bottles_count,
            'num_caves': num_caves
        }

        cursor.close()
        db_connection.close()

        return render_template('accueil.html', user_info=user_info)
    else:
        return render_template('accueil.html')

##############################################################################################
##############################################################################################
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    db_connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

    cursor = db_connection.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and user[2] == password:
        session['username'] = username
        session['user_id'] = user[0]  # Sauvegarde de l'ID de l'utilisateur dans la session
        return redirect("/accueil")
    else:
        notification = Notify()
        notification.title = "IDENTIFIANTS INCORRECTS"
        notification.message = 'Veuillez réessayer !'
        notification.icon = "static/images/notif.png"
        notification.timeout = 5000
        notification.send()

        return redirect("/accueil")

##############################################################################################
##############################################################################################
@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('user_id', None)  # Suppression de l'ID de l'utilisateur de la session
    return redirect("/accueil")

##############################################################################################
##############################################################################################
@app.route("/database_info")
def database_info():
    db_connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

    cursor = db_connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    num_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bottles")
    num_bottles = cursor.fetchone()[0]

    cursor.execute("SELECT username FROM users")
    user_names = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM bottles")
    bottle_names = [row[0] for row in cursor.fetchall()]

    cursor.close()
    db_connection.close()

    return render_template('database_info.html', num_users=num_users, num_bottles=num_bottles, user_names=user_names, bottle_names=bottle_names)

##############################################################################################
##############################################################################################
@app.route("/bouteille", methods=["GET", "POST"])
def bouteille():
    if 'username' in session:
        user_id = session.get('user_id')

        if request.method == "POST":
            winery = request.form.get("winery")
            name = request.form.get("name")
            type = request.form.get("type")
            year = request.form.get("year")
            region = request.form.get("region")
            comments = request.form.get("comments")
            personal_rating = request.form.get("personal_rating")
            community_rating = request.form.get("community_rating")
            price = request.form.get("price")
            shelf_id = request.form.get("shelf_id")

            db_connection = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )

            cursor = db_connection.cursor()

            insert_query = "INSERT INTO bottles (winery, name, type, year, region, comments, personal_rating, community_rating, price, shelf_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            bottle_data = (winery, name, type, year, region, comments, personal_rating, community_rating, price, shelf_id)
            cursor.execute(insert_query, bottle_data)

            db_connection.commit()
            cursor.close()
            db_connection.close()

            return redirect("/accueil")
        else:
            db_connection = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )
            cursor = db_connection.cursor()

            # Récupérer les étagères de l'utilisateur
            get_shelves_query = "SELECT shelf_id, shelf_number FROM shelves WHERE cave_id IN (SELECT cave_id FROM caves WHERE user_id = %s)"
            cursor.execute(get_shelves_query, (user_id,))
            shelves = cursor.fetchall()

            # Récupérer les bouteilles de l'utilisateur
            get_bottles_query = "SELECT * FROM bottles WHERE shelf_id IN (SELECT shelf_id FROM shelves WHERE cave_id IN (SELECT cave_id FROM caves WHERE user_id = %s))"
            cursor.execute(get_bottles_query, (user_id,))
            bottles = cursor.fetchall()

            cursor.close()
            db_connection.close()

            return render_template('bouteille.html', shelves=shelves, bottles=bottles)
    else:
        return redirect("/accueil")
    
##############################################################################################
##############################################################################################
@app.route("/creer_etagere", methods=["GET", "POST"])
def creer_etagere():
    if 'user_id' not in session:
        return redirect("/accueil")  # Rediriger vers la page d'accueil si l'utilisateur n'est pas connecté

    if request.method == "POST":
        shelf_number = request.form.get("shelf_number")
        region = request.form.get("region")
        available_slots = request.form.get("available_slots")
        bottles_per_shelf = request.form.get("bottles_per_shelf")
        user_id = session.get('user_id')  # Récupérer l'ID de l'utilisateur connecté depuis la session

        if not user_id:
            return "Erreur: ID utilisateur invalide."

        db_connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        cursor = db_connection.cursor()

        # Récupérer l'ID de la cave associée à l'utilisateur
        get_cave_id_query = "SELECT cave_id FROM caves WHERE user_id = %s"
        cursor.execute(get_cave_id_query, (user_id,))
        cave_id = cursor.fetchone()[0]

        # Insérer une nouvelle étagère avec l'ID de la cave associée
        insert_query = "INSERT INTO shelves (cave_id, shelf_number, region, available_slots, bottles_per_shelf) VALUES (%s, %s, %s, %s, %s)"
        shelf_data = (cave_id, shelf_number, region, available_slots, bottles_per_shelf)
        cursor.execute(insert_query, shelf_data)

        db_connection.commit()
        cursor.close()
        db_connection.close()

        

        return redirect("/accueil")
    else:
        return render_template("creer_etagere.html")
    
##############################################################################################
##############################################################################################
@app.route("/creer_cave", methods=["GET", "POST"])
def creer_cave():
    if 'user_id' not in session:
        return redirect("/accueil")  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté

    if request.method == "POST":
        cave_name = request.form.get("cave_name")
        user_id = session.get('user_id')

        if not user_id:
            return "Erreur: ID utilisateur invalide."

        db_connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        cursor = db_connection.cursor()

        insert_query = "INSERT INTO caves (user_id, cave_name) VALUES (%s, %s)"
        cave_data = (user_id, cave_name)
        cursor.execute(insert_query, cave_data)

        db_connection.commit()
        cursor.close()
        db_connection.close()

        return redirect("/creer_etagere")
    else:
        return render_template("creer_cave.html")

if __name__ == '__main__':
    app.run(debug=True)

##############################################################################################
##############################################################################################