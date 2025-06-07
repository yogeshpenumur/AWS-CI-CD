from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('staff_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_panel'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template("login.html", form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

<<<<<<< HEAD
@app.route('/student')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('home'))
    return render_template("student_dashboard.html", user=current_user)

@app.route('/staff')
@login_required
def staff_dashboard():
    if current_user.role != 'staff':
        return redirect(url_for('home'))
    return render_template("staff_dashboard.html", user=current_user)

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template("admin_panel.html", users=users)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

if __name__ == "__main__":
    if not os.path.exists("db.sqlite3"):
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=9111)
=======
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=9111)
>>>>>>> 87510099a13e1c58ef972930c509775b8131eff4
