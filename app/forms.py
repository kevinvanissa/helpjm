from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, TextAreaField, HiddenField, IntegerField,FormField, PasswordField, SelectMultipleField,FileField,DateTimeField
from wtforms.validators import Required, Length, Email,EqualTo,ValidationError
from helperlist import CATEGORIES, PARISHES, RATINGS, SCOPE

from app import db

FRIENDSLIST=[
('','-- Choose Friends  --')
]

strip_filter = lambda x: x.strip() if x else None

class LoginForm(Form):
    email = TextField('email',[Required(),Email()])
    password = PasswordField('password',[Required()])

    remember_me = BooleanField('remember_me', default = False)

class ResetPasswordForm(Form):
    oldpassword = PasswordField('oldpassword',[Required()])
    password = PasswordField('password',[Required()])
    confirm = PasswordField('confirm',[
        Required(),
        EqualTo('password',message='Passwords must match')
    ])


class RegistrationForm(Form):
    firstname = TextField('firstname',[Required()])
    lastname = TextField('lastname',[Required()])
    email = TextField('email',[Required(),Email()])
    password = PasswordField('password',[Required()])
    confirm = PasswordField('confirmpassword',[
        Required(),
        EqualTo('password',message='Passwords must match')
    ])



class UserForm(Form):
    firstname = TextField('firstname',[Required()])
    lastname = TextField('lastname',[Required()])
    email = TextField('email',[Required(),Email()])



class AskForm(Form):

    category = SelectField('category',choices=CATEGORIES,validators=[Required()])
    service = SelectField('service',choices=[('','-- Choose a Service --')],validators=[Required()] )
    question = TextAreaField('question', validators = [Required(),Length(min=0, max=140)])
    parish = SelectField('parish',choices=PARISHES,validators=[Required()])
    area = TextField('area',validators=[Required()],filters=[strip_filter])



class FriendForm(Form):
    firstname = TextField('firstname',validators=[Required()])
    lastname = TextField('lastname',validators=[Required()])
    email = TextField('email',validators=[Required()],filters=[strip_filter])


class TelephoneForm(Form):
    country_code = IntegerField('Country Code',validators=[Required()])
    area_code = IntegerField('Area Code',validators=[Required()])
    number = TextField('Number')


def validate_phone(form,field):
    message = "7 digits only please."
    if not field.data.isdigit():
        raise ValidationError(message)
    if int(field.data) > 0000000  and int(field.data) < 9999999 and len(field.data) == 7:
        return True
    else:
        raise ValidationError(message)


class RecommendationForm(Form):
    category = SelectField('category',choices=CATEGORIES,validators=[Required()])
    service = SelectField('service',choices=[('','-- Choose a Service --')],validators=[Required()] )
    name = TextField('name',validators=[Required()],filters=[strip_filter])
    company = TextField('company',filters=[strip_filter])
    phone = TextField('phone',validators=[Required(),validate_phone])
    #phone = FormField(TelephoneForm)
    email = TextField('email',[Email(message="Invalid Email Address")],filters=[strip_filter])
    website = TextField('website',filters=[strip_filter])
    parish = SelectField('parish',choices=PARISHES,validators=[Required()])
    area = TextField('area',validators=[Required()],filters=[strip_filter])
    rating = SelectField('rating',choices=RATINGS,validators=[Required()])
    review = TextAreaField('review', validators = [Length(min=0, max=140)])


class AdForm(Form):
    title = TextField('title',validators=[Required()])
    website = TextField('website',validators=[Required()])
    body = TextAreaField('body', validators = [Length(min=0, max=140),Required()])
    pic = FileField(validators = [Required()])
    ad_start_date = DateTimeField(validators=[Required()])
    ad_end_date = DateTimeField(validators=[Required()])

class AdEditForm(Form):
    title = TextField('title',validators=[Required()])
    website = TextField('website',validators=[Required()])
    body = TextAreaField('body', validators = [Length(min=0, max=140),Required()])
    pic = FileField('pic')
    ad_start_date = DateTimeField(validators=[Required()])
    ad_end_date = DateTimeField(validators=[Required()])


class RecommendationReplyForm(Form):
    name = TextField('name',validators=[Required()])
    company = TextField('company')
    phone = TextField('phone',[Required()])
    user_id = HiddenField('user_id')
    #phone = FormField(TelephoneForm)
    email = TextField('email',[Email(message="Invalid Email Address")])
    website = TextField('website')
    rating = SelectField('rating',choices=RATINGS,validators=[Required()])
    review = TextAreaField('review', validators = [Length(min=0, max=140)])


class ContactUsForm(Form):
    name = TextField('name',validators=[Required()])
    email = TextField('email',validators=[Required(),Email(message="Invalid Email Address")])
    topic = TextField('topic',validators=[Required()])
    message = TextAreaField('message', validators = [Required(),Length(min=0, max=140)])


class SearchForm(Form):
    category = SelectField('category',choices=CATEGORIES,validators=[Required()])
    service = SelectField('service',choices=[('','-- Choose a Service --')],validators=[Required()] )
    parish = SelectField('parish',choices=PARISHES)
    area = TextField('area')
    rating = SelectField('rating',choices=RATINGS)
    recommendedby = SelectField('rating',choices=SCOPE,validators=[Required()])

class ChangePasswordForm(Form):
    email =  TextField('email',[Required(),Email(message="Invalid Email Address")])

class ForgotPasswordForm(Form):
    password = PasswordField('password',[Required()])
    confirm = PasswordField('confirm',[
        Required(),
        EqualTo('password',message='Passwords must match')
    ])



class ReviewForm(Form):
    content = TextAreaField('content', validators = [Required(),Length(min=0, max=140)])
    rating = SelectField('rating',choices=RATINGS)


