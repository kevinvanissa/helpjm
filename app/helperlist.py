from PIL import Image
import os
from app import app

#install python-tz in ubuntu
def convertTime(ltime):
    import pytz, datetime
    local = pytz.timezone ("America/Jamaica")
    #ltime = '2014-10-18 23:37:00'
    naive = datetime.datetime.strptime (ltime, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt


def THUMBER(image, nx=120, ny=120, name='thumb'):
    if image:
        try:
            root, ext = os.path.splitext(image)
            img = Image.open(image)
            thumb = '%s_%s%s' % (root, name, ext)
            img.thumbnail((nx, ny), Image.ANTIALIAS)
            img.save(thumb)
            print "created the thumbnail"
            return thumb
        except Exception as e:
            print "Sending back the orignal image"
            print e
            return image


def RESIZER(image):
    if image:
        try:
            img = Image.open(app.config['UPLOAD_FOLDER'] + image)
            width, height = img.size
            if width >= 600:
                return THUMBER(img, 600, 600)
        except Exception:
            return image
    return image


def createServiceList(filename):
    basedir = os.path.abspath(os.path.dirname(__file__))
    folderpath = basedir+'/services/'
    filename = folderpath+filename
    l = []
    try:
        f = open(filename, 'r')
    except IOError:
        print "Can't open this file"
    else:
        content = f.readlines()
        for c in content:
            c = c.decode('utf-8').rstrip('\n')
            l.append((c, c))
        f.close()
    return l


RECIPE_CATEGORY=[
    ('', '-- Choose a Category --'),
    ('Breakfast','Breakfast'),
    ('Lunch','Lunch'),
    ('Dinner','Dinner'),
    ('Dessert','Dessert'),
    ('Appetizer','Appetizer'),
    ('Drinks','Drinks'),
    ('Snacks','Snacks')
]

RECIPE_SERVINGS=[
    ('', '-- Choose Servings --'),
    ('1 to 2 Servings','1 to 2 Servings'),
    ('2 to 4 Servings','2 to 4 Servings'),
    ('4 to 6 Servings','4 to 6 Servings'),
    ('6 to 8 Servings','6 to 8 Servings'),
    ('8 to 10 Servings','8 to 10 Servings'),
    ('More than 10','More than 10')
]

DAYS=[
    ('', '-- Choose a Day --'),
    ('Sunday','Sunday'),
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday')
]


EVENT_TYPES = [
    ('', '-- Choose a Category --'),
    ('Party','Party'),
    ('Reggae','Reggae'),
    ('Dancehall','Dancehall'),
    ('Gospel','Gospel'),
    ('Festival','Festival'),
    ('Soca','Soca'),
    ('Club','Club'),
    ('Concert','Concert'),
    ('Sport','Sport'),
    ('Art','Art'),
    ('Cuisine', 'Cuisine'),
    ('Fashion','Fashion'),
    ('Theatre','Theatre'),
    ('Charity','Charity'),
    ('Jazz and Blues','Jazz and Blues'),
    ('Lecture','Lecture'),
    ('Fete','Fete'),
    ('Other Events','Other Events')
]


PARISHES = [
    ('', '-- Choose a Parish --'),
    ('Kingston', 'Kingston'),
    ('St. Andrew', 'St. Andrew'),
    ('St. Catherine', 'St. Catherine'),
    ('St. Ann', 'St. Ann'),
    ('St. James', 'St. James'),
    ('Portland', 'Portland'),
    ('Manchester', 'Manchester'),
    ('Clarendon', 'Clarendon'),
    ('St. Thomas', 'St. Thomas'),
    ('St. Mary', 'St. Mary'),
    ('St. Elizabeth', 'St. Elizabeth'),
    ('Trelawny', 'Trelawny'),
    ('Hanover', 'Hanover'),
    ('Westmoreland', 'Westmoreland')
]

SCOPE = [
    ('Anyone', 'Anyone'),
    ('Friends', 'Friends')
]

RATINGS = [
    ('', '-- Choose Rating --'),
    ('Excellent', 'Excellent'),
    ('Very Good', 'Very Good'),
    ('Average', 'Average'),
    ('Poor', 'Poor'),
    ('Terrible', 'Terrible')
]

SERV_AUTO = createServiceList('auto.txt')
SERV_HOME = createServiceList('home.txt')
SERV_WPE = createServiceList('weddingspartiesentertainment.txt')
SERV_PET = createServiceList('pets.txt')
SERV_OUTDOOR = createServiceList('outdoor.txt')
SERV_PDP = createServiceList('physiciandentistpractioners.txt')
SERV_MF = createServiceList('medicalfacilities.txt')
SERV_MR = createServiceList('medicalretailers.txt')
SERV_OTHER = createServiceList('others.txt')
CATEGORIES = [
    ('', '-- Choose a Category --'), ('Home', 'Home'), ('Auto', 'Auto'),
    ('Weddings, Parties, Entertainment', 'Weddings, Parties, Entertainment'),
    ('Pet', 'Pet'), ('Outdoor', 'Outdoor'),
    ('Physicians, Dentists, other Practioners',
     'Physicians, Dentists, other Practioners'),
    ('Medical Facilities', 'Medical Facilities'),
    ('Medical Retailers', 'Medical Retailers'), ('Other', 'Other')]
SERVICESHEADER = [
    ('', '-- Choose a Service --'),
]

SERVICES = SERVICESHEADER + SERV_HOME

CATEGORY = dict()
CATEGORY['Home'] = SERV_HOME
CATEGORY['Auto'] = SERV_AUTO
CATEGORY['Weddings, Parties, Entertainment'] = SERV_WPE
CATEGORY['Pet'] = SERV_PET
CATEGORY['Outdoor'] = SERV_OUTDOOR
CATEGORY['Physicians, Dentists, other Practioners'] = SERV_PDP
CATEGORY['Medical Facilities'] = SERV_MF
CATEGORY['Medical Retailers'] = SERV_MR
CATEGORY['Other'] = SERV_OTHER


def getServiceList(category):
    return CATEGORY[category]


def getServiceListJSON(category):
    servicedict = {}
    servicelist = getServiceList(category)
    for i, s in enumerate(servicelist):
        servicedict[i+1] = s[0]
    return servicedict
