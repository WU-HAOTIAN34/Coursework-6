from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, FileField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=50)])
    password = StringField('password', validators=[DataRequired(), Length(max=50)])
    identity = SelectField('identity', choices=[(0, "User"), (1, 'Administrator')], validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=50)])
    password = StringField('password', validators=[DataRequired(), Length(max=50)])
    name = StringField('password', validators=[DataRequired(), Length(max=50)])
    phone = StringField('password', validators=[DataRequired(), Length(max=50)])
    method = SelectField('identity', choices=[(0, "User"), (1, 'Administrator')], validators=[DataRequired()])


# four conditions for searching the assessments
class AddItemForm(FlaskForm):
    item_name = StringField('item_name', validators=[DataRequired(), Length(max=50)])
    price = IntegerField('price', validators=[DataRequired()])
    description = TextAreaField('release_day', validators=[DataRequired(), Length(max=3000)])
    image = FileField('image')
    submit = SubmitField('Sort')


class PurchaseForm(FlaskForm):
    destination_province = SelectField('destination_province', validators=[DataRequired()])
    destination_city = SelectField('destination_city', validators=[DataRequired()])
    number = IntegerField('number', validators=[DataRequired()])

