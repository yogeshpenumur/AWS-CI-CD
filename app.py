from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, CalculatorForm
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def safe_eval(expr):
    """Evaluate math expressions safely for basic calculator."""
    # Allowed functions and constants
    allowed_names = {
        'abs': abs,
        'round': round,
        'sqrt': math.sqrt,
        'pow': pow,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'log10': math.log10,
        'pi': math.pi,
        'e': math.e,
    }

    # Replace ^ with ** for power
    expr = expr.replace('^', '**')

    # Disallow any dangerous characters
    for char in expr:
        if char not in "0123456789+-*/(). eE^%":
            if char.isalpha():
                # Allow function names
                continue
            else:
                raise ValueError("Invalid character in expression.")

    # Evaluate expression with allowed names only
    return eval(expr, {"__builtins__": {}}, allowed_names)


@app.route('/')
def index():
    return redirect(url_for('calculator'))


@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    form = CalculatorForm()
    result = None
    error = None
    if 'history' not in session:
        session['history'] = []

    if form.validate_on_submit():
        expr = form.expression.data
        try:
            result = safe_eval(expr)
            # Save to history with username for clarity
            session['history'].append(f"{expr} = {result}")
            session.modified = True
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template('calculator.html', form=form, result=result, error=error)


@app.route('/history')
@login_required
def history():
    history = session.get('history', [])
    return render_template('history.html', history=history)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('calculator'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,host='0.0.0.0' ,port=9111)
