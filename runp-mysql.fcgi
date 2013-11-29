#!flask/bin/python

# use mysql
os.environ['DATABASE_URL'] = 'mysql://dundee:gamma.rad4N?@localhost/dundee'

from flup.server.fcgi import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run()
