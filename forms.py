from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,DateTimeField
from wtforms import BooleanField, SelectField, IntegerField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# class RegistrationForm(FlaskForm):
#     username = StringField('Username',validators=[DataRequired(), Length(min=2,max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password')])
#     submit = SubmitField('Sign up')

# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Log in')

class SearchForm(FlaskForm):
    # complete form validatorion
    subreddit = StringField('Subreddit', validators=[DataRequired()])
    term_data = StringField('Term', validators=[DataRequired()])
    category =  SelectField('Category',choices=['Top','Hot','New','Rising',
        'Controversial'],validators=[DataRequired()])
    #limit to a hundred
    num_posts = IntegerField('# of posts to collect',validators=[DataRequired()])
    time_seg = SelectField('Date', choices=['Days','Weeks','Months','Years'],
        validators=[DataRequired()])
    segments = IntegerField('Date Intervals',validators=[DataRequired()])
    after = DateField('Beginning',validators=[DataRequired()] )
    before = DateField('Ending',validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    