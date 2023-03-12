from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, FileField, IntegerField, FloatField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(max=50)])
    identity = SelectField('identity', choices=[(0, "User"), (1, 'Administrator')], validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=50, message="Password should longer than 6!")])
    confirm = PasswordField('confirm', validators=[DataRequired(), Length(min=6, max=50, message="Password should longer than 6!")])
    name = StringField('name', validators=[DataRequired(), Length(max=50)])
    phone = StringField('phone', validators=[DataRequired(), Length(max=50)])
    identity = SelectField('identity', choices=[(0, "User"), (1, 'Administrator')], validators=[DataRequired()])


# four conditions for searching the assessments
class AddItemForm(FlaskForm):
    item_name = StringField('item_name', validators=[DataRequired(message='Item name cannot br empty!'), Length(max=50)])
    price = FloatField('price', validators=[DataRequired(), NumberRange(min=0, max=None, message="Price should be larger than 0!")])
    description = TextAreaField('release_day', validators=[DataRequired(), Length(max=3000)])
    image = FileField('image', validators=[DataRequired()])
    submit = SubmitField('Sort')


class PurchaseForm(FlaskForm):
    destination_province = SelectField('destination_province', validators=[DataRequired()])
    destination_city = SelectField('destination_city', validators=[DataRequired()])
    number = IntegerField('number', validators=[DataRequired()])


class EditItemForm(FlaskForm):
    item_name = StringField('item_name', validators=[DataRequired(message='Item name cannot br empty!'), Length(max=50)])
    price = FloatField('price', validators=[DataRequired(), NumberRange(min=0, max=50, message="Price should be larger than 0!")])
    description = TextAreaField('release_day', validators=[DataRequired(), Length(max=3000)])
    image = FileField('image')
    submit = SubmitField('Sort')


class EditInformationForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=50, message="Password should longer than 6!")])
    name = StringField('password', validators=[DataRequired(), Length(max=50)])
    phone = StringField('password', validators=[DataRequired(), Length(max=50)])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[Length(max=50)])
