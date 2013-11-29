from hashlib import md5
from app import db
from app import app


ROLE_USER = 0
ROLE_ADMIN = 1
ACTIVE_USER = 0
INACTIVE_USER = 1
ACTIVE_ASK = 0
INACTIVE_ASK = 1
ACTIVE_AD = 0
INACTIVE_AD = 1


db.Table('hellosendask',
         db.Column('askid',db.Integer,db.ForeignKey('ask.id')),
         db.Column('friendid',db.Integer,db.ForeignKey('friend.id')),
         db.Column('userid',db.Integer,db.ForeignKey('user.id')),
         db.Column('datesent',db.DateTime)
)


db.Table('helloreplyrecommend',
         db.Column('recommendationid', db.Integer,db.ForeignKey('recommendation.id')),
         db.Column('friendid', db.Integer,db.ForeignKey('friend.id')),
         db.Column('askid', db.Integer,db.ForeignKey('ask.id')),
         db.Column('datesent',db.DateTime)
)

#FIXME: Temporary solution until I understand many to many ternary relationship in SQLAlchemy
class SendAsk(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        askid = db.Column(db.Integer,db.ForeignKey('ask.id'))
        friendid = db.Column(db.Integer,db.ForeignKey('friend.id'))
        userid = db.Column(db.Integer,db.ForeignKey('user.id'))
        datesent = db.Column('datesent',db.DateTime)

        def __repr__(self):
             #FIXME: fix how this model is represented
             return '<SendAsk %r>' % (self.datesent)


class ReplyRecommendation(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        recommendationid = db.Column(db.Integer,db.ForeignKey('recommendation.id'))
        friendid = db.Column(db.Integer,db.ForeignKey('friend.id'))
        askid = db.Column(db.Integer,db.ForeignKey('ask.id'))
        datesent = db.Column(db.DateTime)

        def __repr__(self):
             #FIXME: fix how this model is represented
             return '<ReplyRecommendation %r>' % (self.datesent)

class SendRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recommendationid = db.Column(db.Integer,db.ForeignKey('recommendation.id'))
    friendid = db.Column(db.Integer,db.ForeignKey('friend.id'))
    datesent = db.Column(db.DateTime)

    def __repr__(self):
        return '<SendRecommendation %r>' % (self.datesent)

#----------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    firstname = db.Column(db.String(120),nullable=False)
    lastname = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(140))
    confirmationid = db.Column(db.String(140))
    status = db.Column(db.SmallInteger, default=INACTIVE_USER)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    asks = db.relationship('Ask', backref = 'author', lazy = 'dynamic')
    friends = db.relationship('Friend', backref = 'owner', lazy = 'dynamic')
    #reviews = db.relationship('Review', backref = 'reviewowner', lazy = 'dynamic')
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.status == ACTIVE_USER

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.role == ROLE_ADMIN

    def get_id(self):
        return unicode(self.id)

    def get_confirmationid(self):
        return self.confirmationid

    def __repr__(self):
        return '<User %r>' % (self.email)


class Ask(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(120),nullable=False)
    service = db.Column(db.String(120),nullable=False)
    question = db.Column(db.String(140),nullable=False)
    parish = db.Column(db.Integer,nullable=False)
    area = db.Column(db.String(120),nullable=False)
    created = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger, default=ACTIVE_ASK)

    def is_active(self):
        return self.status == ACTIVE_ASK

    def __repr__(self):
        return '<Ask %r>' % (self.question)


class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    category = db.Column(db.Integer,nullable=False)
    service = db.Column(db.Integer,nullable=False)
    name = db.Column(db.String(120),nullable=False)
    company = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    email = db.Column(db.String(120))
    website = db.Column(db.String(120))
    parish = db.Column(db.Integer,nullable=False)
    area = db.Column(db.String(120),nullable=False)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(140))
    created = db.Column(db.DateTime)
    #allreviews = db.relationship('Review', backref = 'recommendation', cascade = "all,delete", lazy = 'dynamic')

    def __repr__(self):
        return '<Recommend %r>' % (self.review)

#class Review(db.Model):
#    id = db.Column(db.Integer, primary_key = True)
#    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
#    rec_id = db.Column(db.Integer,db.ForeignKey('recommendation.id'))
#    content = db.Column(db.String(140))
#    created = db.Column(db.DateTime)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    firstname = db.Column(db.String(120),nullable=False)
    lastname = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return '<Friend %r>' % (self.firstname)

class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    topic = db.Column(db.String(120),nullable=False)
    message = db.Column(db.String(140),nullable=False)

    def __repr__(self):
        return '<ContactUs %r>' % (self.email)


class Ads(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120),nullable=False)
    website = db.Column(db.String(120))
    body = db.Column(db.String(140),nullable=False)
    pic = db.Column(db.String(1000),nullable=False)
    ad_start_date = db.Column(db.DateTime)
    ad_end_date = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger, default=INACTIVE_AD)
    user_id = db.Column(db.Integer)
    created = db.Column(db.DateTime)


    def __repr__(self):
        return '<Ad %r>' % (self.title)
