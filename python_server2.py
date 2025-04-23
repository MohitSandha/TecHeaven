from flask import Flask, render_template, request, redirect, url_for, flash, g, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session messages (flash)

login_manager = LoginManager()
login_manager.init_app(app)


# 🔹 Function to get a database connection per request
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="localhost",
            user="techheaven",
            password="techie5445",
            database="techheaven_data"
        )
        g.cursor = g.db.cursor(dictionary=True)  # Returns rows as dictionaries
    return g.db, g.cursor

#  Close DB connection at end of request
@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# User Class (For Flask-Login)
class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

# User loader function
@login_manager.user_loader
def load_user(user_id):
    db, cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(id=user["user_id"], email=user["email"])
    return None


# 🔹 Home Route - Render HTML Page
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/categories")
def categories():
    return render_template('categoriesName.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db, cursor = get_db()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            # Flask-Login login
            user_obj = User(id=user['user_id'], email=user['email'])
            login_user(user_obj)  # This tells Flask-Login that the user is authenticated

            # Store user info in session (if you still want to use it)
            session['user_id'] = user['user_id']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['email'] = user['email']

            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials. Try again.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()  # Logs out user from Flask-Login
        session.clear()  # Clears all session data just in case
        flash("You have been logged out.", "info")
    else:
        flash("You are not logged in.", "warning")
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        email = request.form["email"]
        password = request.form["password"]
        
        db, cursor = get_db()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for("signup"))

        # Hash password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Insert new user
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, hashed_password)
        )
        db.commit()

        flash("Signup successful! Please log in.", "success")
        # return redirect(url_for("login"))

    return render_template('signup.html')


@app.route("/cart")
def cart():
    if not session.get('user_id'):
        flash("Please log in. to view cart", "danger")
        return render_template("index.html")
    
   
    db, cursor = get_db()
    print("*" * 150)

    cursor.execute("""
        SELECT 
            c.product_id, 
            c.quantity, 
            p.name, 
            p.price, 
            p.image_url, 
            cat.category_name AS category_name
        FROM 
            cart c
        JOIN 
            products p ON c.product_id = p.product_id
        JOIN 
            categories cat ON p.category_id = cat.category_id
        WHERE 
            c.user_id = %s
    """, (session['user_id'],))

    fetched_cart = cursor.fetchall()
    cartQuantity = len(fetched_cart)

    # Calculate subtotal
    subtotal = sum(item['price'] * item['quantity'] for item in fetched_cart)
    delivery_cost = Decimal(4.99) if subtotal > 0 else 0
    total = subtotal + delivery_cost
    print(fetched_cart)
    
    print("*" * 150)
    return render_template('cart.html',
                           products_in_cart=fetched_cart,
                           cartQuantity=cartQuantity,
                           subtotal=round(subtotal, 2),
                           delivery_cost=round(delivery_cost, 2),
                           total=round(total, 2)
                           )

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    from decimal import Decimal
    data = request.get_json()
    product_id = data['product_id']
    action = data['action']
    user_id = session['user_id']

    db, cursor = get_db()

    # Update the quantity in the cart
    if action == 'increase':
        cursor.execute("""
            UPDATE cart
            SET quantity = quantity + 1
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
    elif action == 'decrease':
        cursor.execute("""
            UPDATE cart
            SET quantity = GREATEST(quantity - 1, 1)
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))

    # Fetch updated quantity for this product
    cursor.execute("SELECT quantity FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    new_quantity = cursor.fetchone()['quantity']

    # Recalculate subtotal, delivery, and total for the entire cart
    cursor.execute("""
        SELECT p.price, c.quantity FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()

    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    delivery_cost = Decimal('4.99') if subtotal > 0 else Decimal('0.00')
    total = subtotal + delivery_cost

    # Recalculate total items in cart
    total_items = sum(item['quantity'] for item in cart_items)

    db.commit()

    return jsonify({
        'new_quantity': new_quantity,
        'subtotal': float(round(subtotal, 2)),
        'delivery_cost': float(round(delivery_cost, 2)),
        'total': float(round(total, 2)),
        'total_items': total_items
    })

@app.route('/categoryView/<category_id>')
def categoryView(category_id):
    print(f"Category is {category_id}")
    db, cursor = get_db()
    cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
    returned_data = cursor.fetchall()
    cursor.execute("SELECT distinct decade FROM products WHERE category_id = %s", (category_id,))
    decades = [x.get('decade') for x in cursor.fetchall()]

    decade1 = []
    decade2 = []
    decade3 = []

    for row in returned_data:
        decade = row.get("decade")
        if decade == decades[0]:
            product_id = row.get("product_id")
            name = row.get("name")
            image_url = row.get("image_url")
            price = row.get("price")
            decade1.append({"product_id": product_id, "name": name, "image_url": image_url, "price": price})

        elif decade == decades[1]:
            product_id = row.get("product_id")
            name = row.get("name")
            image_url = row.get("image_url")
            price = row.get("price")
            decade2.append({"product_id": product_id, "name": name, "image_url": image_url, "price": price})
            
        elif decade == decades[2]:
            product_id = row.get("product_id")
            name = row.get("name")
            image_url = row.get("image_url")
            price = row.get("price")
            decade3.append({"product_id": product_id, "name": name, "image_url": image_url, "price": price})

    print(decade1)
    return render_template(
    "categoryView.html",
    decade1=decade1,
    decade2=decade2,
    decade3=decade3,
    decades=decades,
    category_name="Computer"
)



@app.route('/productView/<product_id>')
def productView(product_id):
    
    db, cursor = get_db()
    cursor.execute("""SELECT 
    p.*, 
    d.cpu, 
    d.mem, 
    d.storage, 
    d.ratings, 
    c.category_name
FROM 
    products p
INNER JOIN 
    product_detail d ON p.product_id = d.product_id
INNER JOIN 
    categories c ON p.category_id = c.category_id
WHERE 
    p.product_id = %s;""", (product_id, ))
    returned_data = cursor.fetchall()[0]
    print(returned_data.keys())
    # returned_data['price'] = Decimal(returned_data['price'])
    return render_template(
        'productView.html',
        product_details=returned_data
        )

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    data = request.get_json()
    product_id = data.get('product_id')
    user_id = session['user_id']

    db, cursor = get_db()

    # Check if item already in cart
    cursor.execute("""
        SELECT quantity FROM cart WHERE user_id = %s AND product_id = %s
    """, (user_id, product_id))
    item = cursor.fetchone()

    if item:
        # Already in cart, increase quantity
        cursor.execute("""
            UPDATE cart SET quantity = quantity + 1 WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
    else:
        # Not in cart, insert new row
        cursor.execute("""
            INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, 1)
        """, (user_id, product_id))

    db.commit()
    return jsonify({'success': True})


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    db, cursor = get_db()
    cursor.execute("""
        DELETE FROM cart WHERE user_id = %s AND product_id = %s;
    """, (session['user_id'], product_id))
    db.commit()

    return jsonify({'success': True})

@app.route('/aboutUs')
def aboutUs():
    
    return render_template('aboutUs.html')

@app.route('/checkout')
def checkOut():
    db, cursor = get_db()
    cursor.execute("""
    select * FROM cart WHERE cart.user_id = %s;
    """, (session['user_id'],))
    
    if len(cursor.fetchall()) == 0:
        
        flash("Please Add Something to cart.", "danger")
            
        return render_template('cart.html')
    return render_template('checkout.html')


@app.route('/redirect')
def redirectPage():
    return render_template('redirectPage.html')

@app.route('/faqPage')
def faqPage():
    return render_template('faqPage.html')

if __name__ == '__main__':


    app.run(host="127.0.0.1", port=8080, debug=True)
