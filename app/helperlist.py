import os
def createServiceList(filename):
    basedir = os.path.abspath(os.path.dirname(__file__))
    folderpath=basedir+'/services/'
    filename = folderpath+filename
    l = []
    try:
        f = open(filename,'r')
    except IOError:
        print "Can't open this file"
    else:
        content = f.readlines()
        for c in content:
            c = c.decode('utf-8').rstrip('\n')
            l.append((c,c))
        f.close()
    return l


PARISHES=[
('','-- Choose a Parish --'),
('Kingston','Kingston'),
('St. Andrew','St. Andrew'),
('St. Catherine','St. Catherine'),
('St. Ann','St. Ann'),
('St. James','St. James'),
('Portland','Portland'),
('Manchester','Manchester'),
('Clarendon','Clarendon'),
('St. Thomas','St. Thomas'),
('St. Mary','St. Mary'),
('St. Elizabeth','St. Elizabeth'),
('Trelawny','Trelawny'),
('Hanover','Hanover'),
('Westmoreland','Westmoreland')
]

SCOPE=[
('Anyone','Anyone'),
('Friends','Friends')
]

RATINGS=[
   ('','-- Choose Rating --'),
   ('Excellent','Excellent'),
   ('Very Good','Very Good'),
   ('Average','Average'),
   ('Poor','Poor'),
   ('Terrible','Terrible')
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
CATEGORIES=[
    ('','-- Choose a Category --'),
    ('Home', 'Home'),
    ('Auto','Auto'),
    ('Weddings, Parties, Entertainment', 'Weddings, Parties, Entertainment'),
    ('Pet', 'Pet'),
    ('Outdoor', 'Outdoor'),
    ('Physicians, Dentists, other Practioners', 'Physicians, Dentists, other Practioners'),
    ('Medical Facilities', 'Medical Facilities'),
    ('Medical Retailers', 'Medical Retailers'),
    ('Other', 'Other')
]
SERVICESHEADER=[
    ('','-- Choose a Service --'),
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



