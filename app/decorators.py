from threading import Thread
from flask import g, flash, redirect, url_for
from functools import wraps

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if  not g.user.is_admin():
            flash("You do not have access to  this page",category='danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

