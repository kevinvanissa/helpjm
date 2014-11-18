import os
from flask_oauth import OAuth

basedir = os.path.abspath(os.path.dirname(__file__))

LOCALHOST_EMAIL=False
#LOCALHOST_EMAIL=True

UPLOAD_FOLDER = basedir+'/app/static/uploads'
ALLOWED_EXTENSIONS = set(['jpg','png','jpeg'])
MAX_CONTENT_LENGTH = 1 * 1024 * 1024

#Facebook
FACEBOOK_APP_ID = '407718329356829'
FACEBOOK_APP_SECRET =  '15b7b78f8813f7ad5e9cffb94d795158'

#Google
# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '864880640386-3p6ncggl7modfn8rckmisl1uvl0itehk.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'eQMe_OLWIGA1R5gD8QRMoAMz'
REDIRECT_URI = '/authorized'


oauth = OAuth()

#facebook
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.google.com/m8/feeds',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)



# pagination
ITEMS_PER_PAGE = 10

CRSF_ENABLED = True
SECRET_KEY = 'tasfh333sdfdssN?*this'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]


#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# mail server settings


if LOCALHOST_EMAIL:
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD =  None
else:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    #MAIL_PORT = 578
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    MAIL_USERNAME = 'admin@dehsuh.com'
    MAIL_PASSWORD = 'gamma.rad4N?'



# administrator list
ADMINS = ['DehSuh Team <admin@dehsuh.com>']


