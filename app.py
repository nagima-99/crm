from flask import render_template, request, redirect, url_for, flash, jsonify
from models import app, db, User, Administrator, Student
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_migrate import Migrate
from forms import StudentForm
from werkzeug.security import generate_password_hash

migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def calculate_age(birth_date):
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


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
            if user.role == 'Администратор':
                return redirect(url_for('administrator_dashboard', id=user.id))
            elif user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))
        else:
            flash('Неправильное имя пользователя или пароль')

    return render_template('login.html')

@app.route('/administrator/<int:id>', methods=['GET', 'POST'])
@login_required
def administrator_dashboard(id):
    
    administrator = Administrator.query.filter_by(id=id).first()

    if administrator.role != 'Администратор':
        return redirect(url_for('login'))
    
    age = calculate_age(administrator.birth_date)

    if request.method == 'POST':

        if 'username' in request.form:
            administrator.username = request.form['username']
        if 'email' in request.form:
            administrator.email = request.form['email']
        if 'phone' in request.form:
            administrator.phone = request.form['phone']
        if 'address' in request.form:
            administrator.address = request.form['address']
        if 'main_office' in request.form:
            administrator.main_office = request.form['main_office']
        if 'additional_offices' in request.form:
            administrator.additional_offices = request.form['additional_offices']

        db.session.commit()
        flash('Данные успешно обновлены!')
        return redirect(url_for('administrator_dashboard', id=administrator.id))

    administrator_data = {
        'id': administrator.id,
        'username': administrator.username,
        'birth_date': age,
        'role': administrator.role,
        'email': administrator.email,
        'phone': administrator.phone,
        'address': administrator.address,
        'main_office': administrator.main_office,
        'additional_offices': administrator.additional_offices
    }
    return render_template('administrator_dashboard.html', administrator=administrator_data)
    
@app.route('/manage_courses')
@login_required
def manage_courses():
    if current_user.role == 'Администратор':
        administrator = Administrator.query.filter_by(id=current_user.id).first()
        return render_template('manage_courses.html', username=current_user.username, administrator=administrator)
    else:
        return redirect(url_for('login'))

@app.route('/manage_groups')
@login_required
def manage_groups():
    if current_user.role == 'Администратор':
        administrator = Administrator.query.filter_by(id=current_user.id).first()
        return render_template('manage_groups.html', username=current_user.username, administrator=administrator)
    else:
        return redirect(url_for('login'))
     
@app.route('/manage_students')
@login_required
def manage_students():
    if current_user.role == 'Администратор':
        administrator = Administrator.query.filter_by(id=current_user.id).first()
        return render_template('manage_students.html', username=current_user.username, administrator=administrator)
    else:
        return redirect(url_for('login')) 

@app.route('/manage_teachers')
@login_required
def manage_teachers():
    if current_user.role == 'Администратор':
        administrator = Administrator.query.filter_by(id=current_user.id).first()
        return render_template('manage_teachers.html', username=current_user.username, administrator=administrator)
    else:
        return redirect(url_for('login'))   

@app.route('/manage_schedaule')
@login_required
def manage_schedaule():
    if current_user.role == 'Администратор':
        administrator = Administrator.query.filter_by(id=current_user.id).first()
        return render_template('manage_schedaule.html', username=current_user.username, administrator=administrator)
    else:
        return redirect(url_for('login'))   
    
@app.route('/create_student', methods=['GET', 'POST'])
@login_required
def create_student():
    if current_user.role != 'Администратор':
        return redirect(url_for('index'))

    administrator = Administrator.query.filter_by(id=current_user.id).first()

    form = StudentForm()

    if form.validate_on_submit():
        existing_student = Student.query.filter_by(email=form.email.data).first()
        if existing_student:
            flash('Этот email уже зарегистрирован. Пожалуйста, используйте другой.', 'error')
            return render_template('create_student.html', form=form, administrator=administrator)

        new_student = Student(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            birth_date=form.birth_date.data,
            phone=form.phone.data,
            address=form.address.data,
            client_name=form.client_name.data,
            client_relation=form.client_relation.data,
            client_phone=form.client_phone.data,
            client_workplace=form.client_workplace.data,
            client_position=form.client_position.data
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Студент успешно добавлен!', 'success')
        return redirect(url_for('create_student'))
    else:
        print(form.errors)

    return render_template('create_student.html', form=form, administrator=administrator)


@app.route('/teacher')
@login_required
def teacher_dashboard():
    if current_user.role == 'teacher':
        return render_template('teacher_dashboard.html', username=current_user.username)
    else:
        return redirect(url_for('login'))

@app.route('/student')
@login_required
def student_dashboard():
    if current_user.role == 'student':
        return render_template('student_dashboard.html', username=current_user.username)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, threaded=True)
    