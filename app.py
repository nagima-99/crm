from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '00cb48ff0bb190c58724e6b3834ced90'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login.html') 

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        session['username'] = user.username
        session['role'] = user.role

        if user.role == 'manager':
            return redirect(url_for('manager_dashboard'))
        elif user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        elif user.role == 'student':
            return redirect(url_for('student_dashboard'))
    else:
        return 'Неправильный логин или пароль', 401

@app.route('/manager')
def manager_dashboard():
    if 'role' in session and session['role'] == 'manager':
        return render_template('manager_dashboard.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/teacher')
def teacher_dashboard():
    if 'role' in session and session['role'] == 'teacher':
        return render_template('teacher_dashboard.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/student')
def student_dashboard():
    if 'role' in session and session['role'] == 'student':
        return render_template('student_dashboard.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)