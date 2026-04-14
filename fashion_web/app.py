from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret"

# Sample products
products = [
    {"id": 1, "name": "Red T-Shirt", "price": 500, "category": "top"},
    {"id": 2, "name": "Blue Jeans", "price": 1200, "category": "bottom"},
    {"id": 3, "name": "Black Shoes", "price": 2000, "category": "footwear"},
    {"id": 4, "name": "White Shirt", "price": 800, "category": "top"},
    {"id": 5, "name": "Sneakers", "price": 1500, "category": "footwear"}
]

# HOME PAGE
@app.route('/')
def home():
    return render_template("home.html", products=products)

# ADD TO CART
@app.route('/add/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(id)
    return redirect('/')

# VIEW CART
@app.route('/cart')
def cart():
    cart_items = [p for p in products if p['id'] in session.get('cart', [])]
    return render_template("cart.html", items=cart_items)

# CATEGORY FILTER
@app.route('/category/<cat>')
def category(cat):
    filtered = [p for p in products if p['category'] == cat]
    return render_template("home.html", products=filtered)

# SEARCH
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    result = [p for p in products if query.lower() in p['name'].lower()]
    return render_template("home.html", products=result)

# RECOMMENDATION
def recommend(product_id):
    for p in products:
        if p['id'] == product_id:
            return [x for x in products if x['category'] == p['category'] and x['id'] != product_id]
    return []

@app.route('/product/<int:id>')
def product_page(id):
    selected = next((p for p in products if p['id'] == id), None)
    recs = recommend(id)
    return render_template("home.html", products=[selected], recs=recs)

if __name__ == "__main__":
    app.run(debug=True)