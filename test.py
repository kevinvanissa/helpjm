#!flask/bin/python
import os
import unittest
from config import basedir
from app import app, db
from datetime import datetime, timedelta
from werkzeug import check_password_hash, generate_password_hash,secure_filename
import os,uuid
from app.models import User, ROLE_USER, ROLE_ADMIN,ACTIVE_ASK,INACTIVE_ASK, INACTIVE_USER,ACTIVE_USER,Ask, Friend, Recommendation,ContactUs,SendAsk,ReplyRecommendation,Ads,SendRecommendation
from werkzeug.datastructures import ImmutableMultiDict


from coverage import coverage
cov = coverage(branch = True, omit = ['flask/*','test.py'])
cov.start()


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_noaccess(self):
        rv = self.app.get('/main')
        assert 'redirected' in rv.data

    def login(self, email, password,remember_me):
        return self.app.post('/index', data=dict(
            email=email,
            password=password,
            remember_me=remember_me
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)



    def test_login_logout(self):
        rv = self.login('kevinvanissa@gmail.com', 'password123', False)
        assert 'This email is not recognized' in rv.data
        u1 = User(firstname="Kevin",
                    lastname="Miller",
                    email="kevinvanissa@gmail.com",
                    password=generate_password_hash("password123"),confirmationid=str(uuid.uuid4()))
        db.session.add(u1)
        db.session.commit()
        rv = self.login('kevinvanissa@gmail.com', 'password123', False)
        assert 'confirm your registration' in rv.data
        u1.status = ACTIVE_USER
        db.session.add(u1)
        db.session.commit()
        rv = self.login('kevinvanissa@gmail.com', 'password123', False)
        assert 'successfully logged in' in rv.data
        rv = self.logout()
        assert 'You have successfully logged out' in rv.data
        rv = self.login('kevinvanissa@gmail.com', 'defaultx', False)
        assert 'Please check your username and password' in rv.data

    def add_friend(self,firstname,lastname,email):
        rv = self.app.post('/friends', data=dict(
            firstname=firstname,
            lastname=lastname,
            email=email
        ), follow_redirects=True)
        #if firstname and lastname and email:
        #    assert 'Your friend is now Created' in rv.data
        return rv

    def edit_user(self,firstname,lastname,email):
        rv = self.app.post('/edit', data=dict(
            firstname=firstname,
            lastname=lastname,
            email=email
        ), follow_redirects=True)
        return rv

    def reset_password(self,oldpassword,password,confirm):
        rv = self.app.post('/reset', data=dict(
            oldpassword=oldpassword,
            password=password,
            confirm=confirm
        ), follow_redirects=True)
        return rv

    def add_ask(self,category,service,question,parish,area):
        rv = self.app.post('/main',data=dict(
            category=category,
            service=service,
            question=question,
            parish=parish,
            area=area
        ), follow_redirects=True)
        #Send To Friends
        #Your Ask was successfully sent! You will be notfied by email when there are responses
        #check for the question etc in /main
        return rv

    def add_recommendation(self,category,service,name,company,phone,email,
                           website,parish,area,rating,review):
        rv = self.app.post('/recommendations',data=dict(
            category=category,
            service=service,
            name=name,
            company=company,
            phone=phone,
            email=email,
            website=website,
            parish=parish,
            area=area,
            rating=rating,
            review=review
        ), follow_redirects=True)
        return rv



    def send_ask(self,allvalues):
        rv = self.app.post('/sendtofriends',data=allvalues,follow_redirects=True)
        return rv


    def test_edit_user(self):
        u1 = User(firstname="Kevin",
                    lastname="Miller",
                    email="kevinvanissa@gmail.com",
                    password=generate_password_hash("password123"),confirmationid=str(uuid.uuid4()))

        u1.status = ACTIVE_USER
        db.session.add(u1)
        db.session.commit()

        self.login('kevinvanissa@gmail.com', 'password123', False)
        #edit user
        v = self.edit_user("Kevin","Miller","sdundee@yahoo.com")
        assert 'Your changes have been saved.' in v.data
        u2 = User(firstname="Vanissa",
                    lastname="Miller",
                    email="sassyvanjay@yahoo.com",
                    password=generate_password_hash("123password123"),confirmationid=str(uuid.uuid4()))

        u2.status = ACTIVE_USER
        db.session.add(u2)
        db.session.commit()
        self.login('sassyvanjay@yahoo.com', '123password123', False)
        v1 = self.edit_user("Vanissa","Simmonds","sassyvanjay@yahoo.com")
        assert 'Sorry but this email is already registered at HelpJM!' in v1.data



    def test_add_recommendation(self):
        u1 = User(firstname="Kevin",
                    lastname="Miller",
                    email="kevinvanissa@gmail.com",
                    password=generate_password_hash("password123"),confirmationid=str(uuid.uuid4()))

        u1.status = ACTIVE_USER
        db.session.add(u1)
        db.session.commit()

        self.login('kevinvanissa@gmail.com', 'password123', False)
        v = self.add_recommendation("Home","Plumbing","Mr. Bogle","Old Navy",
                                    "8787876","madagain@yahoo.com",
                                    "www.maddog.com","Kingston","Stand Pipe",
                                    "Excellent","He is quite Good")
        assert 'Your Recommendation is now created!' in v.data


    def test_reset_password(self):
        u1 = User(firstname="Kevin",
                    lastname="Miller",
                    email="kevinvanissa@gmail.com",
                    password=generate_password_hash("password123"),confirmationid=str(uuid.uuid4()))

        u1.status = ACTIVE_USER
        db.session.add(u1)
        db.session.commit()

        self.login('kevinvanissa@gmail.com', 'password123', False)
        #reset password without problems
        v = self.reset_password("password123","pass123","pass123")
        assert "Your password was successfully reset!" in v.data
        #reset password wrong old password
        v1 = self.reset_password("password123","pass123","pass123")
        assert "Your old password is incorrect!" in v1.data
        #reset but passwords don't match
        v2 = self.reset_password("pass123","pass276","pass")
        assert "[Passwords must match]" in v2.data



    def test_add_friend(self):
        u1 = User(firstname="Kevin",
                    lastname="Miller",
                    email="kevinvanissa@gmail.com",
                    password=generate_password_hash("password123"),confirmationid=str(uuid.uuid4()))

        u1.status = ACTIVE_USER
        db.session.add(u1)
        db.session.commit()

        self.login('kevinvanissa@gmail.com', 'password123', False)
        v = self.add_friend('Kevin','Miller','kevinvanissa@gmail.com')
        assert 'Your friend is now Created' in v.data
        assert 'Kevin Miller' in v.data

        # add friend with the same email address
        v1 = self.add_friend('Dundee','Mill','kevinvanissa@gmail.com')
        assert 'You already have a friend with this email!' in v1.data

        # add another friend and see if two friends are there
        v2 = self.add_friend('Vanissa','Miller','sassyvanjay@yahoo.com')
        assert 'Your friend is now Created' in v2.data

        #check if friend was added
        rv = self.app.get('/friends',follow_redirects=True)
        assert 'kevinvanissa@gmail.com' in rv.data
        assert 'sassyvanjay@yahoo.com' in rv.data


    def test_send_add_ask(self):
        self.test_add_friend()
        #check if we have access in another test
        rv = self.app.get('/friends',follow_redirects=True)
        assert 'kevinvanissa@gmail.com' in rv.data
        rv1 = self.add_ask(category='Home',service='Plumbing',question='Need a cheap one',
                           parish='Kingston',area='Half Way Tree')
        assert 'Send To Friends' in rv1.data
        assert 'Kevin' in rv1.data
        assert 'Vanissa' in rv1.data

        #Send Ask
        allvalues=ImmutableMultiDict([('btn',u'send'),('emailfriends',u'1'),('emailfriends',u'2')])
        #mybtn=('btn',u'send')
        rv2 = self.send_ask(allvalues)
        #print rv2.data
        assert 'Your Ask was successfully sent! You will be notified by email when there are responses' in rv2.data
        assert 'Need a cheap one' in rv2.data

        rv3 = self.app.get('/more/1',follow_redirects=True)
        assert 'Kevin' in rv3.data
        assert 'Vanissa' in rv3.data
        assert '[No one has replied to your Ask as yet]' in rv3.data
        assert 'Home' in rv3.data
        assert 'Plumbing' in rv3.data
        assert 'Kingston' in rv3.data
        assert 'Half Way Tree' in rv3.data
        assert 'Need a cheap one' in rv3.data

    def test_delete_friend_after_add_ask(self):
        self.test_send_add_ask()

        #delete friend, remember friends set from test_send_add_ask
        allvalues1=ImmutableMultiDict([('friends',u'1')])
        rv = self.app.post('/deletemultiplefriends',data=allvalues1,follow_redirects=True)
        assert 'You have deleted the selected friends' in rv.data
        rv1 = self.app.get('/more/1',follow_redirects=True)
        assert 'Kevin' not in rv1.data
        assert 'Vanissa' in rv1.data

        #with app.test_client() as c:
        #    with c.session_transaction() as sess:
        #        sess['user_id'] = u1.id
        #        sess['_fresh'] = True
        #        rv = self.addfriendform('Kevin','Miller','kevinvanissa@gmail.com')
        #        print rv.data
        #        assert 'Your friend is now Created' in rv.data


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    coverage_bool=False
    if coverage_bool:
        cov.stop()
        cov.save()
        print "\n\nCoverage Report: \n"
        cov.report()
        print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
        cov.html_report(directory = "tmp/coverage")
        cov.erase()
