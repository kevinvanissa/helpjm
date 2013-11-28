from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS
from decorators import async

@async
def send_async_email(msg):
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)

def ask_notification(friend, user, ask):
    send_email("[HelpJM] %s %s needs a good %s?" % (user.firstname,user.lastname,ask.service),
        ADMINS[0],
        [friend.email],
        render_template("ask_email.txt",
            friend = friend, user = user,ask=ask),
        render_template("ask_email.html",
            friend = friend, user = user, ask=ask))


def recommendation_notification(friend,user,ask,recommendationid):
    send_email("[HelpJM] %s %s has a recommendation for you" % (friend.firstname,friend.lastname),
        ADMINS[0],
        [user.email],
        render_template("recommendation_email.txt",
            friend = friend, user = user,ask=ask,recid=recommendationid),
        render_template("recommendation_email.html",
            friend = friend, user = user, ask=ask,recid=recommendationid))


def recommendation_notification2(friend,user,ask,recList):
    send_email("[HelpJM] %s %s has recommendations for you" % (friend.firstname,friend.lastname),
        ADMINS[0],
        [user.email],
        render_template("recommendation2_email.txt",
            friend = friend, user = user,ask=ask,recList=recList),
        render_template("recommendation2_email.html",
            friend = friend, user = user, ask=ask,recList=recList))


def sendrec_notification(friend,user,recommendation):
    send_email("[HelpJM] %s %s has a recommendation for you" % (user.firstname,user.lastname),
        ADMINS[0],
        [friend.email],
        render_template("sendtofriend_recommendation_email.txt",
            friend = friend, user = user,recommendation=recommendation),
        render_template("sendtofriend_recommendation_email.html",
            friend = friend, user = user,recommendation=recommendation))


def user_confirmation_notification(user):
    send_email("[HelpJM] Registration Confirmation for %s %s " % (user.firstname,user.lastname),
        ADMINS[0],
        [user.email],
        render_template("confirmation_email.txt", user = user),
        render_template("confirmation_email.html", user = user))


def forgot_password_notification(user):
    send_email("[HelpJM] Password Recovery",
        ADMINS[0],
        [user.email],
        render_template("forgot_password_email.txt", user = user),
        render_template("forgot_password_email.html", user = user))






