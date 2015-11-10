from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS
from decorators import async


@async
def send_async_email(msg):
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)


def ask_notification(friend, user, ask):
    send_email(
        "[ServiceJA] %s %s needs good %s services ?" %
        (user.firstname, user.lastname, ask.service), ADMINS[0], [
            friend.email], render_template(
            "emails/ask_email.txt", friend=friend, user=user, ask=ask), render_template(
            "emails/ask_email.html", friend=friend, user=user, ask=ask))


def thankyou_notification(friend, user, recommendation, message):
    send_email(
        "[ServiceJA] %s %s is thanking you for the Recommendation that you sent." %
        (user.firstname,
         user.lastname),
        ADMINS[0],
        [
            friend.email],
        render_template(
            "emails/thankyou_email.txt",
            friend=friend,
            user=user,
            recommendation=recommendation,
            message=message),
        render_template(
            "emails/thankyou_email.html",
            friend=friend,
            user=user,
            recommendation=recommendation,
            message=message))


def recommendation_notification(friend, user, ask, recommendationid):
    send_email(
        "[ServiceJA] %s %s has a recommendation for you" %
        (friend.firstname,
         friend.lastname),
        ADMINS[0],
        [
            user.email],
        render_template(
            "emails/recommendation_email.txt",
            friend=friend,
            user=user,
            ask=ask,
            recid=recommendationid),
        render_template(
            "emails/recommendation_email.html",
            friend=friend,
            user=user,
            ask=ask,
            recid=recommendationid))


def recommendation_notification2(friend, user, ask, recList):
    send_email(
        "[ServiceJA] %s %s has recommendations for you" %
        (friend.firstname,
         friend.lastname),
        ADMINS[0],
        [
            user.email],
        render_template(
            "emails/recommendation2_email.txt",
            friend=friend,
            user=user,
            ask=ask,
            recList=recList),
        render_template(
            "emails/recommendation2_email.html",
            friend=friend,
            user=user,
            ask=ask,
            recList=recList))


def sendrec_notification(friend, user, recommendation):
    send_email(
        "[ServiceJA] %s %s has a recommendation for you" %
        (user.firstname,
         user.lastname),
        ADMINS[0],
        [
            friend.email],
        render_template(
            "emails/sendtofriend_recommendation_email.txt",
            friend=friend,
            user=user,
            recommendation=recommendation),
        render_template(
            "emails/sendtofriend_recommendation_email.html",
            friend=friend,
            user=user,
            recommendation=recommendation))


def user_confirmation_notification(user):
    send_email(
        "[ServiceJA] Registration Confirmation for %s %s " %
        (user.firstname, user.lastname), ADMINS[0], [
            user.email], render_template(
            "emails/confirmation_email.txt", user=user), render_template(
            "emails/confirmation_email.html", user=user))


def forgot_password_notification(user):
    send_email("[ServiceJA] Password Recovery",
               ADMINS[0],
               [user.email],
               render_template("emails/forgot_password_email.txt", user=user),
               render_template("emails/forgot_password_email.html", user=user))
