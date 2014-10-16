#!flask/bin/python

from app import app
print 'Remember to change local_email to False and app.config files:init and config'
app.run(debug=True)

#app.run(host = '0.0.0.0')
