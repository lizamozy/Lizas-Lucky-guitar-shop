import sqlite3
from flask import Flask, render_template, request, session, redirect, flash, url_for

app = Flask('app')
#making secret key
app.secret_key = "my_key"


@app.route('/', methods=['POST', 'GET'])
def home():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if (request.method == 'POST'):
        x = request.form["query"]
        cursor.execute("SELECT * FROM products WHERE prod_name LIKE ?",
                       ("%" + x + "%", ))
        get_query = cursor.fetchall()
        cursor.execute("SELECT DISTINCT(category) FROM products")
        category = cursor.fetchall()
        return render_template("search.html",get_products=get_query, get_category=category)
    else:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        cursor.execute("SELECT DISTINCT(category) FROM products")
        category = cursor.fetchall()

        connection.commit()
        connection.close()

        return render_template("home.html",
                               get_products=products,
                               get_category=category)


# route to get the individual products in each category
@app.route('/category/<cat>')
def cats(cat):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products WHERE category=?", (cat, ))
    products = cursor.fetchall()

    cursor.execute("SELECT DISTINCT(category) FROM products")
    category = cursor.fetchall()

    connection.commit()
    connection.close()

    return render_template("home.html",
                           get_products=products,
                           get_category=category)


@app.route('/cart/add', methods=['POST', 'GET'])
def add_to_cart():

    prod_id = request.form['prod_id']
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    #if user is not signed in, take them to the sign in page if they click add to cart
    if 'name' not in session:
        print("not in session")
        return redirect(url_for('login'))
    #check if cart is not in session,
    if 'cart' not in session:
        session["cart"] = {}

    if (request.method == 'POST'):

        cursor.execute("SELECT * FROM products WHERE prod_id=? ",
                       (request.form['prod_id'], ))
        product = cursor.fetchone()

        connection.commit()
        connection.close()

        if prod_id not in session["cart"].keys():
            session["cart"][prod_id] = 1
        else:
            session["cart"][prod_id] += 1

        if (int(product["stock"]) < session["cart"][prod_id]):
            session["cart"][prod_id] = product["stock"]

        elif (int(product["stock"]) <= 0):
            flash("Cannot Add Item to Cart")

    session["cart"] = session["cart"]
    #want to go to the cart page
    return redirect("/view_cart")


##this function is not working and when i exit the page it doesnt close
@app.route('/view_cart', methods=['POST', 'GET'])
def view_cart():
    cart = list()
    cart_total = 0
    if 'cart' not in session:
        return redirect("/cart/add")

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    for item in session["cart"]:
        print(item)
        cursor.execute(
            "SELECT prod_id, prod_name, prod_color,stock, price FROM products WHERE prod_id=? ",
            (item, ))
        product = cursor.fetchone()

        current = {}
        current["prod_id"] = product["prod_id"]
        current["prod_name"] = product["prod_name"]
        current["price"] = product["price"]
        current["stock"] = product["stock"]
        current["prod_color"] = product["prod_color"]
        current["prod_id"] = product["prod_id"]
        current["quant"] = session["cart"][item]
        current["total"] = current["quant"] * current["price"]
        cart_total += current["total"]
        cart.append(current)

    return render_template("view_cart.html", cart=cart, cart_total=cart_total)


#function to remove one from cart
@app.route("/cart/remove", methods=['POST', 'GET'])
def remove():

    id = request.form['prod_id']

    if request.method == 'POST':
        if 'cart' in session:
            session["cart"][id] -= 1
        if session["cart"][id] == 0:

            flash("No more Items to Remove")

    session["cart"] = session["cart"]
    #want to go to the cart page
    return redirect("/view_cart")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the username/password is correct, log them in and redirect them to the home page. Remember to set your session variables!
    if 'user' in session:
        return redirect("/")

    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        session.clear()
        # connect to database
        connection = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # try to find student based on username and password
        cursor.execute(
            "SELECT username, password FROM users WHERE username=? AND password=?",
            (request.form["username"], request.form["password"]))
        user = cursor.fetchone()

        # commit and close database connection
        connection.commit()
        connection.close()

        # if user is set, username and password are correct
        if user:
            # Username and password correct, set session variables and redirect
            session['name'] = user['username']
            #print(session["name"])
            session['password'] = user['password']

            return redirect(url_for("home"))
        else:
            # Login credentials incorrect, flash error message
            flash('Username and/or password incorrect')
    # return the login page (on failed login or GET)
    return render_template("login.html")


#logout route
@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect("/")


##method to clear the cart
@app.route("/clear_cart", methods=['GET', 'POST'])
def clear_cart():
    session.pop("cart", None)
    return redirect("/")


#method to go back home
@app.route("/go_home", methods=['GET', 'POST'])
def go_home():
    if request.method == 'POST':
        return redirect("/")


#checkout method
@app.route("/checkout", methods=['GET', 'POST'])
def checkout():

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    print("I made it")
    if request.method == 'POST':
        total = 0
        for item in session['cart']:
            print(item)
            cursor.execute("SELECT * FROM products where prod_id =?",
                           (item, ))
            product = cursor.fetchone()
            print("I made it again ")
            #check the stock in the database against quantity in cart
            if product["stock"] < session["cart"][item]:
                session["cart"][item] = product['stock']

            #update the stock inside of the database
            stock = product["stock"] 
            stock -= session["cart"][item]
            cursor.execute("UPDATE products SET stock=? WHERE prod_id=?", (stock,item))
            total += session['cart'][item] * product['price']
       #inserts the order into the database
        user = session['name']
        cursor.execute("INSERT INTO orders (user_id, cost) VALUES (?,?)", (user, total))

      #popping the cart after we save the order
        connection.commit()
        connection.close()
      
        session.pop("cart", None)
    return render_template("checkout.html")

#route to view past orders
#add button in home page to go to past orders, goes to this route, and displays all of the past orders
@app.route("/view_orders", methods=['GET','POST'])
def view_orders():
  connection = sqlite3.connect("database.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  if 'name' not in session:
    return redirect("/login")
  cursor.execute("SELECT * FROM orders WHERE user_id=?", (session['name'],))
  past_ords = cursor.fetchall()

  return render_template("past_orders.html", past_ords=past_ords)

#route to create a new account
@app.route("/create_login", methods=['GET', 'POST'])
def create_acc():

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if request.method() == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?,?,?)", (
                username,
                password,
                email,
            ))

    connection.commit()
    connection.close()

    return render_template("login.html")


app.run(host='0.0.0.0', port=8080)
