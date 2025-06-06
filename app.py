from flask import Flask, render_template, redirect, url_for, request, session
from models import db, Product, User, create_admin
from forms import LoginForm
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

@app.before_first_request
def setup():
    db.create_all()
    create_admin()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart)).all()
    total = sum(p.price for p in products)
    return render_template('cart.html', products=products, total=total)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=9111)