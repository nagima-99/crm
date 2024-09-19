from flask import render_template, request, redirect, url_for, flash
from models import app, db, User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            if user.role == 'manager':
                return redirect(url_for('manager_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))
        else:
            flash('Неправильное имя пользователя или пароль')

    return render_template('login.html')

@app.route('/manager')
@login_required
def manager_dashboard():
    if current_user.role == 'manager':
        return render_template('manager_dashboard.html', current_user.username)
    else:
        return redirect(url_for('login'))

@app.route('/teacher')
@login_required
def teacher_dashboard():
    if current_user.role == 'teacher':
        return render_template('teacher_dashboard.html', current_user.username)
    else:
        return redirect(url_for('login'))

@app.route('/student')
@login_required
def student_dashboard():
    if current_user.role == 'student':
        return render_template('student_dashboard.html', current_user.username)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)