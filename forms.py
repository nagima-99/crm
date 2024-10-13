from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class StudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    client_name = StringField('Client Name', validators=[DataRequired()])
    client_relation = StringField('Client Relation', validators=[DataRequired()])
    client_phone = StringField('Client Phone', validators=[DataRequired()])
    client_workplace = StringField('Client Workplace', validators=[DataRequired()])
    client_position = StringField('Client Position', validators=[DataRequired()])

    submit = SubmitField('Create Student')
