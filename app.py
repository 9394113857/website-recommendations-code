from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommendations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)
    page = db.Column(db.String(50), nullable=False)
    interaction_time = db.Column(db.String(19), nullable=False)  # Assuming interaction_time is stored as text in ISO 8601 format 'YYYY-MM-DD HH:MM:SS'


def create_database():
    if not os.path.exists('recommendations.db'):
        with app.app_context():
            db.create_all()

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if existing_user:
            error = 'User already exists. Please login.'
            return render_template('login.html', error=error)
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect to login page after registration
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/record_interaction', methods=['POST'])
def record_interaction():
    if 'user_id' in session:
        try:
            user_id = session['user_id']
            data = request.get_json()
            action = data.get('action')
            page = data.get('page')

            if action and page:
                # Generate current timestamp
                interaction_time = datetime.now()

                new_interaction = UserActivity(user_id=user_id, action=action, page=page, interaction_time=interaction_time)
                db.session.add(new_interaction)
                db.session.commit()
                return 'Interaction recorded successfully'
            else:
                return 'Invalid data received for recording interaction', 400  # Bad request status code
        except Exception as e:
            return f'Error recording interaction: {str(e)}', 500  # Internal server error status code
    else:
        return 'User not logged in', 401  # Unauthorized status code


if __name__ == '__main__':
    create_database()
    create_tables()
    app.run(debug=True)
