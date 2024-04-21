from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = '0.0.0.0'  # Adresse IP de votre serveur MySQL
app.config['MYSQL_PORT'] = 3306  # Port du serveur MySQL
app.config['MYSQL_USER'] = 'root'  # Nom d'utilisateur MySQL
app.config['MYSQL_PASSWORD'] = 'Ryanbaba73'  # Mot de passe MySQL
app.config['MYSQL_DB'] = 'website_projet'  # Nom de la base de données MySQL

# Route pour afficher la liste des bouteilles
@app.route("/")
def main():
    return render_template('index.html',template_folder='templates')

# Route pour afficher le formulaire d'inscription
@app.route("/signup", methods=["GET"])
def signup_form():
    return render_template('signup.html')

# Route pour gérer la soumission du formulaire d'inscription
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    # Connexion à la base de données MySQL en utilisant les configurations de l'application Flask
    db_connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

    # Création d'un curseur pour exécuter des requêtes SQL
    cursor = db_connection.cursor()

    # Insertion des données de l'utilisateur dans la table users
    insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    user_data = (username, password)
    cursor.execute(insert_query, user_data)

    # Validation de la transaction et fermeture du curseur et de la connexion à la base de données
    db_connection.commit()
    cursor.close()
    db_connection.close()

    # Rediriger vers la page de connexion après l'inscription réussie
    return redirect("/login")

@app.route("/database_info")
def database_info():
    # Connexion à la base de données MySQL
    db_connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

    # Création d'un curseur pour exécuter des requêtes SQL
    cursor = db_connection.cursor()

    # Exécutez les requêtes SQL pour récupérer les informations souhaitées de votre base de données
    cursor.execute("SELECT COUNT(*) FROM users")
    num_users = cursor.fetchone()[0]  # Nombre d'utilisateurs

    cursor.execute("SELECT COUNT(*) FROM bottles")
    num_bottles = cursor.fetchone()[0]  # Nombre de bouteilles

    # Récupérer les noms des utilisateurs
    cursor.execute("SELECT username FROM users")
    user_names = [row[0] for row in cursor.fetchall()]  # Liste des noms d'utilisateurs

    # Récupérer les noms des bouteilles
    cursor.execute("SELECT name FROM bottles")
    bottle_names = [row[0] for row in cursor.fetchall()]  # Liste des noms de bouteilles

    # Fermez le curseur et la connexion à la base de données
    cursor.close()
    db_connection.close()

    # Renvoyez les informations récupérées au modèle HTML pour affichage
    return render_template('database_info.html', num_users=num_users, num_bottles=num_bottles, user_names=user_names, bottle_names=bottle_names)

if __name__ == '__main__':
    app.run(debug=True)
