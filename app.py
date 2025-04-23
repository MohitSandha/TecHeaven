from flask import Flask, render_template, request, redirect
import mysql.connector
# import MySQLdb

app = Flask(__name__)

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="mohit",       
    password="12345678", 
    database="myDB" 
)
cursor = db.cursor()

# Home Route - Render HTML Page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure you have an "index.html" file

@app.route("/categories")
def categories():
    return render_template('categoriesName.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
