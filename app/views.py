from datetime import datetime, timedelta,date
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_from_directory, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm, EventSearchForm, CommentForm, AskForm, FriendForm, RecommendationForm, UserForm, ContactUsForm, SearchForm, RecommendationReplyForm, RegistrationForm, ResetPasswordForm, ChangePasswordForm, AdForm, AdEditForm, ForgotPasswordForm, ReviewForm, MessageForm, MainSearchForm, SearchForm2, EventForm, EventEditForm,RecipeForm, RecipeSearchForm
from models import User, Comment, ROLE_USER, FEATURED_EVENT, NOFEATURED_EVENT, ROLE_ADMIN, ACTIVE_ASK, INACTIVE_ASK, INACTIVE_USER, ACTIVE_USER, Ask, Friend, Recommendation, ContactUs, SendAsk, ReplyRecommendation, Ads, SendRecommendation, Review, Event, ACTIVE_EVENT, INACTIVE_EVENT, MealPlan, Recipe
from config import ITEMS_PER_PAGE, ALLOWED_EXTENSIONS, facebook, google, REDIRECT_URI
from helperlist import convertTime, EVENT_TYPES, PARISHES, SERVICES, CATEGORIES, getServiceList, getServiceListJSON, THUMBER
from emails import ask_notification, recommendation_notification, recommendation_notification2, user_confirmation_notification, forgot_password_notification, sendrec_notification, thankyou_notification
from werkzeug import check_password_hash, generate_password_hash, secure_filename
import os
import time, calendar
import uuid
from decorators import admin_required
import random
import urllib
import sys
import getopt
import getpass
from sqlalchemy import or_
from sqlalchemy.sql import extract
import sqlalchemy
from functools import reduce
import pytz
from sqlalchemy.orm import aliased

# Render Json
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

    
@login_required
def getAds1():
    return [1, 2, 3]


def getAds():
    all_ads = list(Ads.query.all())
    random.shuffle(all_ads)
    return all_ads[:3]


#===============================Calendar ==================

def getFirstDay(year,month):
    daycount=0
    cal = calendar.Calendar(6)
    month_days = cal.itermonthdays(year,month)
    for day in month_days:
        if not day:
            daycount = daycount + 1
        else:
            break
    return daycount


@app.route('/displaycal', methods=['GET', 'POST'])
def displaycal():
#def createCalendar(year, month, change):
    mnames = "Placeholder January February March April May June July August September October November December"
    mnames = mnames.split()
    #copied from previous function
    year = request.form["year"]
    month = request.form["month"]
    change = request.form["change"]


    if (year == "None" or month == "None"):
        year, month = time.localtime()[:2]
    else:
        year=int(year)
        month=int(month)
        change=change
        if change in ("next", "prev"):
            now, mdelta = date(year,month,15), timedelta(days=31)
            if change == "next": mod = mdelta
            elif change == "prev": mod = -mdelta
            year, month = (now+mod).timetuple()[:2]

    cal = calendar.Calendar(6)
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst=[[]]
    week = 0
    count = 0

    for day in month_days:
        count = count + 1
        entries = current = False
        if day:
            events = Event.query.filter(
                    extract('year',Event.event_start_date) == year,
                    extract('month',Event.event_start_date) == month,
                extract('day',Event.event_start_date) == day
            ).first()
            if events:
                entries = True
            #if event_type:
                #entries = db(db.event.event_start_date.day()==day) (db.event.event_start_date.month()==month) (db.event.event_start_date.year()==year) (db.event.event_type==event_type).select()
            #else:
                #entries = db(db.event.event_start_date.day()==day) (db.event.event_start_date.month()==month) (db.event.event_start_date.year()==year).select()
            #pass
            if day == nday and year == nyear and month == nmonth:
                current = True
        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1
        firstDayMonth = getFirstDay(year, month)
        padcalendar1 = 42 - count
        padcalendar = range(padcalendar1)
        padfeb= range(7)

    prev ="\"prev\""
    next ="\"next\""
    none ="\"None\""

    table = "<div class='myCalendar'>"
    table += "<table id='calTable' width=100% >"
    table += "<tr id='calHeader1'><td class='myHover'><a href='javascript:getCalendar("+str(year)+","+str(month)+","+prev+")'><img src='/static/img/prev.png'></a></td><td colspan='5' style='text-align:center;'>"+mnames[month]+" "+str(year)+"</td><td class='myHover'><a href='javascript:getCalendar("+str(year)+","+str(month)+","+next+")'><img src='/static/img/next.png'></a></td></tr>"
    table+="<tr id='calHeader'>"
    table+="<th><span style='color:red;'>Sun</span></th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th><span style='color:red;'>Sat</span></th>"
    table+="</tr>"
    count = 0

    #calDict = createCalendar(year,month,change)
    #for week in calDict['month_days']:
    for week in lst:
        count = count + 1
        table+="<tr>"
        for day, events, current in week:
            if events:
                table+="<td class='myHover'><a href='javascript:showEvents("+str(year)+","+str(month)+","+str(day)+") '><b><span class='cevents'>"+str(day)+"</span></b></a></td>"
            elif current:
                table+="<td class='today myHover'>"+str(day)+"</td>"
            elif(day == 0):
                table+="<td><span class='hidezero'>"+str(day)+"</span></td>"
            else:
                table+="<td class='myHover'>"+str(day)+"</td>"
            #print day, current
        table+= "</tr>"


    table+="</table>"
    table += ""
    table+="</div>"
    table+="<div class='calFooter'><table id='calTable2' width='100%'><tr><td><a class='btn btn-default' href='javascript:getCalendar("+none+","+none+","+none+")'>Today</a></td></tr></table></div>"
    #print count

    #return dict(year=year,month=month, month_days=lst, mname=mnames[month],
            #padcalendar=padcalendar,
            #firstDayMonth=firstDayMonth,padfeb=padfeb
            #)
    return table
#===============================Calendar ==================

#===============================START RECIPE ==================
@app.route('/createrecipe', methods=['GET','POST'])
@login_required
def createrecipe():
    form = RecipeForm()
    if form.validate_on_submit():
        filename = ""
        file = request.files['picture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename=str(uuid.uuid4())+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        else:
            flash('Only jpeg, jpg or png files are accepted',category='danger')
            return redirect(url_for('createrecipe'))
        recipe=Recipe(
                name=form.name.data,
                serving=form.serving.data,
                category=form.category.data,
                description=form.description.data,
                ingredients=form.ingredients.data,
                instructions=form.instructions.data,
                picture=filename,
                user_id=g.user.id,
                created=datetime.now()
                )
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe was created',category='success')
        return redirect(url_for('createrecipe'))

    return render_template("recipe/createrecipe.html",
            title='Create Recipe',
            form=form
            )



@app.route('/mealplan', methods=['GET','POST'])
@login_required
def mealplan():
    DAYS=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']    
    breakfast = list(Recipe.query.filter_by(category='Breakfast').all())
    random.shuffle(breakfast)
    #breakfast = breakfast[:1]
    breakfast = breakfast[:7]

    lunch = list(Recipe.query.filter_by(category='Lunch').all())
    random.shuffle(lunch)
    lunch = lunch[:7]

    dinner = list(Recipe.query.filter_by(category='Dinner').all())
    random.shuffle(dinner)
    dinner = dinner[:7]
    
    #buttonclicked = request.args.get("mbtn")
    buttonclicked = request.form.get("mbtn")
    if buttonclicked:
        db.session.query(MealPlan).delete()
        db.session.commit()

    meals = MealPlan.query.all()

    if not meals:
        for index, day in enumerate(DAYS):
            if index<len(breakfast):
                mealPlanBreakfast = MealPlan(recipe_id=breakfast[index].id,day=day,user_id=g.user.id)
                db.session.add(mealPlanBreakfast)
            if index<len(lunch):
                mealPlanLunch = MealPlan(recipe_id=lunch[index].id,day=day,user_id=g.user.id)
                db.session.add(mealPlanLunch)
            if index<len(dinner):
                mealPlanDinner = MealPlan(recipe_id=dinner[index].id,day=day,user_id=g.user.id)
                db.session.add(mealPlanDinner)
            db.session.commit()
        """
        mealPlanBreakfast = MealPlan(recipe_id=1,day='Sunday',user_id=g.user.id)
        mealPlanLunch = MealPlan(recipe_id=2,day='Sunday',user_id=g.user.id)
        mealPlanDinner = MealPlan(recipe_id=3,day='Sunday',user_id=g.user.id)
        db.session.add(mealPlanBreakfast)
        db.session.add(mealPlanLunch)
        db.session.add(mealPlanDinner)
        db.session.commit()
        """

    recipes = db.session.query(Recipe,MealPlan).filter(Recipe.id==MealPlan.recipe_id,MealPlan.user_id==g.user.id).all()
    

    return render_template("recipe/mealplan.html",
            title='Meal Plan',
            recipes=recipes,
            days=DAYS
            )

@app.route('/recipe/<int:id>', methods=['GET'])
@login_required
def recipedetail(id):
    recipe = Recipe.query.get_or_404(int(id))
    ingredients = (recipe.ingredients).split('\n')
    instructions = (recipe.instructions).split('\n')
    return render_template("recipe/recipedetail.html",
            title='Recipe Detail',
            recipe=recipe,
            ingredients=ingredients,
            instructions=instructions
            )   

@app.route('/shoppinglist', methods=['GET'])
@login_required
def shoppinglist():
    ingredients=[]
    ingredients2=[]
    items = db.session.query(MealPlan,Recipe).filter(MealPlan.recipe_id==Recipe.id).all()
    for item in items:
        ingredients.append((item.Recipe.ingredients).split('\n'))
    for ingredient in ingredients:
        for i in ingredient:
            k=i.split()[2:]
            if k:
                joined = ' '.join(k)
                if joined  not in ingredients2:
                    ingredients2.append(joined) 
            
    return render_template("recipe/shoppinglist.html",
            title='Shopping List',
            ingredients2=ingredients2
            )

@app.route('/recipesearch', methods=['GET','POST'])
@login_required
def recipesearch():
    form = RecipeSearchForm()
    name = request.args.get("name")
    category = request.args.get("category")
    buttonclicked = request.args.get("mybtn")
    query_dict= dict()

    if not buttonclicked:
        return render_template(
            'recipe/recipesearch.html',
            title='Search Recipe',
            form=form,
            recipes=[],
            queries=[],
            btnclicked=None)

    queries_without_page = request.args.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']
    
    if category:
        query_dict['category'] = category

    recipes = Recipe.query.filter_by(**query_dict)
    query_list = []
    if name:
        name = name.split()
        for n in name:
            query_list.append(Recipe.name.ilike("%"+n+"%"))
            query_list.append(Recipe.category.ilike("%"+n+"%"))
        recipes = recipes.filter(
                reduce(
                    lambda a, b:(
                        a | b),query_list))
    
    try:
        page = int(request.args.get("page",'1'))
    except ValueError:
        page=1
    recipes = recipes.order_by(Recipe.name).paginate(page, ITEMS_PER_PAGE, False)
    
    return render_template(
        'recipe/recipesearch.html',
        title='Recipe Search',
        form=form,
        recipes=recipes,
        queries=urllib.urlencode(queries_without_page),
        btnclicked=True)

#===============================END RECIPE ==================

@app.route('/main', methods=['GET', 'POST'])
@login_required
def index():
    user = User.query.filter_by(id=g.user.id).first()
    asks = Ask.query.filter_by(
        user_id=user.id,
        status=ACTIVE_ASK).order_by("created desc").all()
    #asks = user.asks.all()
    #asks = asks.query.filter_by(status=ACTIVE_ASK).all()
    ads = getAds()
    form = AskForm()
    if request.method == 'POST':
        if form.category.data:
            form.service.choices = getServiceList(form.category.data)
        if form.validate_on_submit():
            session['category'] = form.category.data
            session['service'] = form.service.data
            session['question'] = form.question.data
            session['parish'] = form.parish.data
            session['area'] = form.area.data
            session['created'] = datetime.now()
            return redirect(url_for('sendtofriends'))

    return render_template("asks/asks.html",
                           title='Home',
                           form=form,
                           asks=asks,
                           ads=ads
                           )

    
    
@app.route('/closedasks', methods=['GET', 'POST'])
@login_required
def closedasks():
    form = AskForm()
    asks = Ask.query.filter_by(
        user_id=g.user.id,
        status=INACTIVE_ASK).order_by("created desc").all()
    ads = getAds()
    return render_template(
        "asks/closedasks.html",
        title="Closed Asks",
        asks=asks,
        ads=ads,
        form=form)


@app.route('/more/<int:id>', methods=['GET', 'POST'])
@login_required
def more(id):
    reviewForm = ReviewForm()
    messageForm = MessageForm()
    frienddict = dict()
    form = AskForm()
    ask = Ask.query.filter_by(id=int(id)).first()
    form.service.choices = getServiceList(ask.category)
    form.category.data = ask.category
    form.service.data = ask.service
    form.question.data = ask.question
    form.parish.data = ask.parish
    form.area.data = ask.area

    friends = db.session.query(
        Friend,
        SendAsk).filter(
        SendAsk.friendid == Friend.id,
        SendAsk.askid == int(id)).all()
    for f in friends:
        if f.Friend in frienddict:
            frienddict[f.Friend] = frienddict[f.Friend] + 1
            continue
        frienddict[f.Friend] = 1

    #recommendations = db.session.query(ReplyRecommendation,Friend).filter(ReplyRecommendation.friendid == Friend.id,ReplyRecommendation.askid == int(id)).all()
    recommendations = db.session.query(
        ReplyRecommendation,
        Friend,
        Recommendation).filter(
        ReplyRecommendation.friendid == Friend.id,
        ReplyRecommendation.askid == int(id),
        Recommendation.id == ReplyRecommendation.recommendationid).all()
    return render_template(
        "asks/more.html",
        title="More",
        recommendations=recommendations,
        form=form,
        frienddict=frienddict,
        messageForm=messageForm,
        reviewForm=reviewForm,
        id=id)


@app.route(
    '/createreview/<int:recommendationid>/<int:askid>',
    methods=[
        'GET',
        'POST'])
@login_required
def createreview(recommendationid, askid):
    reviewForm = ReviewForm()
    if reviewForm.validate_on_submit():
        review = Review(
            user_id=g.user.id,
            rec_id=recommendationid,
            review=reviewForm.review.data,
            created=datetime.now(),
            rating=reviewForm.rating.data)
        db.session.add(review)
        db.session.commit()
        flash(
            'Your Review was successfully created! You should now be able to view it when you click the view link below!',
            category='success')
        return redirect(url_for('more', id=askid))
    flash(
        'You need to fill in all the fields before we can send this Review',
        category='danger')
    return redirect(url_for('more', id=askid))


@app.route(
    '/sendthankyou/<int:friendid>/<int:recommendationid>/<int:askid>',
    methods=[
        'GET',
        'POST'])
@login_required
def sendthankyou(friendid, recommendationid, askid):
    user = User.query.filter_by(id=g.user.id).first()
    friend = Friend.query.filter_by(id=int(friendid)).first()
    recommendation = Recommendation.query.filter_by(
        id=int(recommendationid)).first()
    messageForm = MessageForm()
    if messageForm.validate_on_submit():
        thankyou_notification(
            friend,
            user,
            recommendation,
            messageForm.message.data)
        flash(
            'Your thank you message was successfully sent to %s!' %
            friend.firstname,
            category='success')
        return redirect(url_for('more', id=askid))
    flash(
        'You need to write a message before we can send this message to %s!' %
        friend.firstname,
        category='danger')
    return redirect(url_for('more', id=askid))


@app.route('/sendtofriends', methods=['GET', 'POST'])
@login_required
def sendtofriends():
    # print request.form
    friendlist = request.form.getlist('emailfriends')
    ads = getAds()
    user = User.query.filter_by(id=g.user.id).first()
    friends = user.friends.order_by(Friend.firstname).all()
    if not friendlist and request.form.get('btn') == 'send':
        flash("You need to select at least one friend", category='info')
        return redirect(url_for('sendtofriends'))
    if friendlist and request.form.get('btn') == 'send':
        ask = Ask(
            user_id=g.user.id,
            category=session['category'],
            service=session['service'],
            question=session['question'],
            parish=session['parish'],
            area=session['area'],
            created=session['created'])
        db.session.add(ask)
        db.session.commit()
        for r in friendlist:
            friend = Friend.query.filter_by(id=int(r)).first()
            ask_notification(friend, user, ask)
            sendask = SendAsk(
                askid=ask.id,
                friendid=friend.id,
                userid=user.id,
                datesent=datetime.now())
            db.session.add(sendask)
            db.session.commit()
        del session['category']
        del session['service']
        del session['question']
        del session['parish']
        del session['area']
        del session['created']
        flash(
            'Your Ask was successfully sent! You will be notified by email when there are responses',
            category='success')
        return redirect(url_for('index'))
    return render_template(
        "friends/sendtofriends.html",
        friends=friends,
        title="Send to Friends",
        ads=ads)


@app.route('/sendtofriendsagain/<int:id>', methods=['GET', 'POST'])
@login_required
def sendtofriendsagain(id):
    friendlist = request.form.getlist('emailfriends')
    ads = getAds()
    sendasklist = list()
    user = User.query.filter_by(id=g.user.id).first()
    ask = Ask.query.filter_by(id=int(id)).first()
    sendasks = SendAsk.query.filter_by(askid=ask.id).all()
    for s in sendasks:
        sendasklist.append(s.friendid)
    friends = user.friends.order_by(Friend.firstname).all()
    if not friendlist and request.form.get('btn') == 'send':
        flash("You need to select at least one friend", category='info')
        return redirect(url_for('sendtofriendsagain', id=ask.id))
    if friendlist:
        for r in friendlist:
            friend = Friend.query.filter_by(id=int(r)).first()
            ask_notification(friend, user, ask)
            sendask = SendAsk(
                askid=ask.id,
                friendid=friend.id,
                userid=user.id,
                datesent=datetime.now())
            db.session.add(sendask)
            db.session.commit()
        flash(
            'Your Ask was successfully resent! You will be notified by email when there are responses',
            category='success')
        return redirect(url_for('index'))
    return render_template(
        'friends/sendtofriendsagain.html',
        friends=friends,
        title='Send to friends',
        sendasks=sendasklist,
        id=id,
        ads=ads)


@app.route('/sendrectofriends/<int:id>', methods=['GET', 'POST'])
@login_required
def sendrectofriends(id):
    friendlist = request.form.getlist('emailfriends')
    ads = getAds()
    user = User.query.filter_by(id=g.user.id).first()
    recommendation = Recommendation.query.filter_by(id=int(id)).first()
    friends = user.friends.order_by(Friend.firstname).all()
    if not friendlist and request.form.get('btn') == 'send':
        flash("You need to select at least one friend", category='info')
        return redirect(url_for('sendrectofriends', id=recommendation.id))
    if friendlist:
        for r in friendlist:
            friend = Friend.query.filter_by(id=int(r)).first()
            sendrec_notification(friend, user, recommendation)
            sendrec = SendRecommendation(
                recommendationid=recommendation.id,
                friendid=friend.id,
                datesent=datetime.now())
            db.session.add(sendrec)
            db.session.commit()
        flash('Your Recommendation was successfully sent!', category='success')
        return redirect(url_for('recommendations'))
    return render_template(
        'friends/sendrectofriend.html',
        friends=friends,
        title='Send Recommendation to friends',
        id=id,
        ads=ads)


@app.route('/closeask/<int:id>', methods=['GET', 'POST'])
@login_required
def closeask(id):
    ask = Ask.query.filter_by(id=int(id)).first()
    if ask.user_id == g.user.id:
        ask.status = INACTIVE_ASK
        db.session.add(ask)
        db.session.commit()
        sAsk = SendAsk.query.filter_by(askid=ask.id).all()
        for s1 in sAsk:
            db.session.delete(s1)
            db.session.commit()
        rReply = ReplyRecommendation.query.filter_by(askid=ask.id).all()
        for r1 in rReply:
            db.session.delete(r1)
            db.session.commit()
    return redirect(url_for('index'))


@app.route('/reopenask/<int:id>', methods=['GET', 'POST'])
@login_required
def reopenask(id):
    ask = Ask.query.filter_by(id=int(id)).first()
    if ask.user_id == g.user.id:
        ask.status = ACTIVE_ASK
        ask.created = datetime.now()
        db.session.add(ask)
        db.session.commit()
    return redirect(url_for('closedasks'))


@app.route('/deleteask/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteask(id):
    ask = Ask.query.filter_by(id=int(id)).first()
    if not ask:
        abort(404)
    if ask.user_id == g.user.id:
        db.session.delete(ask)
        db.session.commit()
        flash("Your ask is now deleted", category='success')
    return redirect(url_for('closedasks'))


# FIXME: for ask and recommendation you should click more and information
# hide/show
@app.route('/recommendations', methods=['GET', 'POST'])
@login_required
def recommendations():
    #user = User.query.filter_by(id = g.user.id).first()
    #recommendations = user.recommendations.all()
    ads = getAds()
    recommendations = Recommendation.query.filter_by(
        user_id=g.user.id).order_by("created desc").all()
    form = RecommendationForm()
    if request.method == 'POST':
        if form.category.data:
            form.service.choices = getServiceList(form.category.data)
        if form.validate_on_submit():
            recommendation = Recommendation(
                user_id=g.user.id,
                category=form.category.data,
                service=form.service.data,
                name=form.name.data,
                company=form.company.data,
                phone=form.phone.data,
                email=form.email.data,
                website=form.website.data,
                parish=form.parish.data,
                area=form.area.data,
                rating=form.rating.data,
                review=form.review.data,
                created=datetime.now())
            db.session.add(recommendation)
            db.session.commit()
            flash("Your Recommendation is now created!", category='success')
            return redirect(url_for('recommendations'))
    return render_template("recommendations/recommendations.html",
                           title='Recommendations',
                           form=form,
                           recommendations=recommendations,
                           ads=ads)


@app.route('/servicelist', methods=['GET', 'POST'])
def servicelist():
    d = getServiceListJSON(request.form['category'])
    return jsonify(d)


@app.errorhandler(404)
def internal_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(413)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/413.html'), 413

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    # if g.user.is_authenticated():
    #    g.user.last_seen = datetime.now()
    #    db.session.add(g.user)
    #    db.session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    mform = MainSearchForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('There is already a user with this email!', category='danger')
            return redirect(url_for('register'))
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=generate_password_hash(
                form.password.data),
            confirmationid=str(
                uuid.uuid4()))
        db.session.add(user)
        db.session.commit()
        # Send email for confirmation
        user_confirmation_notification(user)
        flash(
            'Thanks for registering. Please check your email to confirm',
            category='info')
        return redirect(url_for('login'))
    return render_template(
        'users/register.html',
        title='Register',
        form=form,
        mform=mform)


@app.route('/activate_user/<confirmationid>', methods=['GET', 'POST'])
def activate_user(confirmationid):
    found_user = User.query.filter_by(confirmationid=confirmationid).first()
    if not found_user:
        return abort(404)
    else:
        if found_user.status == INACTIVE_USER:
            found_user.status = ACTIVE_USER
            db.session.add(found_user)
            db.session.commit()
            flash(
                'User has been activated. You can now log in your account!',
                category='success')
            return redirect(url_for('login'))
        elif found_user.status == ACTIVE_USER:
            flash('User already activated!', category='info')
        return redirect(url_for('login'))


def splitfacebookname(fullname):
    name = fullname.split()
    firstname = name[0]
    lastname = " ".join(name[1:])
    return (firstname, lastname)


def splitgooglecontacts(contact):
    firstname = ""
    lastname = ""
    info = contact.split('-')
    email = info[1]
    name = info[0].split()
    if name:
        firstname = name[0]
        lastname = " ".join(name[1:])
    return (email, firstname, lastname)


def parse_contact(contact):
    if u'gd$email' in contact:
        emails = []
        for e in contact[u'gd$email']:
            emails.append(e.get(u'address'))
        return {
            'name': contact.get('title', {}).get('$t', ''),
            'emails': emails
        }
    else:
        return None


#---------------google-----------------

@app.route('/importcontacts', methods=['GET', 'POST'])
@login_required
def importcontacts():
    contacts = request.form.getlist('friends')
    if not contacts:
        flash('You need to select at least one friend', category='info')
        return redirect(url_for('googlecontacts'))
    for c in contacts:
        email, firstname, lastname = splitgooglecontacts(c)
        friend = Friend.query.filter_by(email=email).first()
        if friend and friend.owner.id == g.user.id:
            pass
        else:
            if firstname == "" and lastname == "":
                pass
            else:
                f = Friend(
                    user_id=g.user.id,
                    firstname=firstname,
                    lastname=lastname,
                    email=email)
                db.session.add(f)
                db.session.commit()
    flash('Your google contacts were successfully imported', category='info')
    return redirect(url_for('friends'))


@app.route('/googlecontacts')
def googlecontacts():
    contactlist = []
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}

    start = 1
    data = None
    res = None

    while start == 1 or 'entry' in data['feed']:
        req = Request(
            'https://www.google.com/m8/feeds/contacts/default/full?alt=json&max-results=50&start-index=%s' %
            start,
            None,
            headers)
        try:
            res = urlopen(req)
        except URLError as e:
            if e.code == 401:
                # Unauthorized - bad token
                session.pop('access_token', None)
                return redirect(url_for('loging'))
            return res.read()
        import json
        data = json.loads(res.read())
        if 'entry' in data['feed'] and len(data['feed']['entry']):
            for entry in data['feed']['entry']:
                contact = parse_contact(entry)
                if contact:
                    contactlist.append(contact)
        start += 50
    res.close()
    return render_template(
        'googlecontacts/importcontacts.html',
        title='Import Contacts',
        contactlist=contactlist)


@app.route('/logingoogle')
def loging():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('googlecontacts'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


#-----------facebook-----------------------
@app.route('/loginfacebook', methods=['GET', 'POST'])
def loginf():
    return facebook.authorize(
        callback=url_for(
            'facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))


@app.route('/loginfacebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        flash(
            'Access denied: reason=%s error=%s' %
            (request.args['error_reason'],
             request.args['error_description']),
            category='danger')
        return redirect(url_for('login'))
        # return 'Access denied: reason=%s error=%s' % (
           # request.args['error_reason'],
           # request.args['error_description']
        #)
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    if me.data['email'] is None or me.data['email'] == "":
        flash('Invalid login. Please try again')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=me.data['email']).first()
    if user is None:
        firstname, lastname = splitfacebookname(me.data['name'])
        user = User(email=me.data['email'],
                    firstname=firstname,
                    lastname=lastname,
                    confirmationid=str(uuid.uuid4()),
                    status=ACTIVE_USER)
        #user.status = ACTIVE_USER
        #user.confirmationid = str(uuid.uuid4())
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash('You have successfully logged in', category='success')
    return redirect(request.args.get('next') or url_for('index'))
    # return 'Logged in as id=%s name=%s  email=%s redirect=%s' % \
    #    (me.data['id'], me.data['name'],me.data['email'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')



@app.route('/login2', methods=['GET', 'POST'])
def login2():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('events'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(
                'The username or password you entered is incorrect!',
                category='danger')
            return redirect(url_for('login2'))
        if user.status == INACTIVE_USER:
            flash(
                'You need to confirm your registration before you log in!',
                category='info')
            return redirect(url_for('login2'))
        if user.password is None or user.password == "":
            flash(
                'The username or password you entered is incorrect!',
                category='danger')
            return redirect(url_for('login2'))
        if user and check_password_hash(user.password, form.password.data):
            session['remember_me'] = form.remember_me.data
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            flash('You have successfully logged in', category='success')
            return redirect(request.args.get('next') or url_for('events'))
        else:
            flash('Please check your username and password!', category='danger')
            return redirect(url_for('login2'))
    #return render_template('users/loginBackup.html',
    return render_template('users/login2.html',
                           title='Log In',
                           form=form
                           )




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    mform = MainSearchForm()
    sform = EventSearchForm()
    #nyear, nmonth, nday = time.localtime()[:3]
    #nowtoday = datetime.now()
    #year = nowtoday.year
    #month = nowtoday.month
    #day = nowtoday.day
    #tomorrow = nowtoday + timedelta(days=1)
    #day2 =  tomorrow.day
    #month2 = tomorrow.month
    #year2 = tomorrow.year
    #tomorrow = tomorrow.replace(hour=23, minute=59, second=59,microsecond=0)

    #featuredEvents = Event.query.filter_by(featured=FEATURED_EVENT).all()

    #todayEvents = Event.query.filter(
    #        extract('year',Event.event_start_date) == year,
    #        extract('month',Event.event_start_date) == month,
    #        extract('day',Event.event_start_date) == day
    #    ).limit(5).all()

    #tomorrowEvents = Event.query.filter(
    #        extract('year',Event.event_start_date) == year2,
    #        extract('month',Event.event_start_date) == month2,
    #        extract('day',Event.event_start_date) == day2
    #    ).limit(5).all()
    #Same as Future Events
    #upcomingEvents = Event.query.filter(Event.event_start_date > tomorrow).limit(5).all()

    #comments = db.session.query(
    #            Comment,Event
    #).filter(Comment.event_id==Event.id).order_by(Comment.created.desc()).limit(3).all()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(
                'The username or password you entered is incorrect!',
                category='danger')
            return redirect(url_for('login'))
        if user.status == INACTIVE_USER:
            flash(
                'You need to confirm your registration before you log in!',
                category='info')
            return redirect(url_for('login'))
        if user.password is None or user.password == "":
            flash(
                'The username or password you entered is incorrect!',
                category='danger')
            return redirect(url_for('login'))
        if user and check_password_hash(user.password, form.password.data):
            session['remember_me'] = form.remember_me.data
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            flash('You have successfully logged in', category='success')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Please check your username and password!', category='danger')
            return redirect(url_for('login'))
    #return render_template('users/loginBackup.html',
    return render_template('users/login.html',
                           title='Sign In',
                           form=form,
                           mform=mform,
                           sform=sform)
                           #todayEvents=todayEvents,
                           #featuredEvents=featuredEvents
                           #upcomingEvents=upcomingEvents,
                           #tomorrowEvents=tomorrowEvents,
                           #comments=comments)


@app.route('/mainsearch', methods=['GET', 'POST'])
def mainsearch():
    ads = getAds()
    form = SearchForm2()
    mform = MainSearchForm()

    mainsearch = request.args.get("mainsearch")
    parish = request.args.get("parish")

    queries_without_page = request.args.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']

    recommendations = Recommendation.query
    query_list = []

    if parish:
        recommendations = recommendations.filter_by(parish=parish)

    if mainsearch:
        main_search_list = mainsearch.split()
        for t in main_search_list:
            query_list.append(Recommendation.category.ilike("%"+t+"%"))
            query_list.append(Recommendation.service.ilike("%"+t+"%"))
            #recommendations = recommendations.filter(Recommendation.category.ilike("%"+t+"%"))
            #recommendations = recommendations.filter(Recommendation.service.ilike("%"+t+"%"))
    # FIXME: This worked below
    #recommendations = Recommendation.query.filter(Recommendation.category.contains("Pet"))
    #recommendations = recommendations.filter(Recommendation.category.ilike("%Pet%"))
    recommendations = recommendations.filter(
        reduce(
            lambda a, b: (
                a | b), query_list))

    try:
        page = int(request.args.get("page", '1'))
    except ValueError:
        page = 1

    #recommendations = recommendations.paginate(page,ITEMS_PER_PAGE,False)
    recommendations = recommendations.order_by(
        sqlalchemy.sql.expression.case(
            ((Recommendation.rating == "Excellent", 1),
             (Recommendation.rating == "Very Good", 2),
                (Recommendation.rating == "Average", 3),
                (Recommendation.rating == "Poor", 4),
                (Recommendation.rating == "Terrible", 5)))).paginate(
        page, ITEMS_PER_PAGE, False)

    return render_template(
        'search/mainsearch.html',
        title='Search Results',
        form=form,
        recommendations=recommendations,
        ads=ads,
        queries=urllib.urlencode(queries_without_page),
        mform=mform)


@app.route('/mainsearch2', methods=['GET', 'POST'])
def mainsearch2():
    form = SearchForm2()
    name = request.args.get("name")
    category = request.args.get("category")
    #service = form.service.data
    service = request.args.get("service")
    parish = request.args.get("parish")
    area = request.args.get("area")
    rating = request.args.get("rating")
    buttonclicked = request.args.get("mybtn")
    query_dict = dict()

    if not buttonclicked:
        return render_template(
            'search/mainsearch.html',
            title='Search',
            form=form,
            recommendations=[],
            queries=[],
            btnclicked=None
            )

    queries_without_page = request.args.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']

    # if not category or not service and request.args.get("btn") == "sendsearch":
    #    flash("Please enter at least the Category and Service!",category='danger')
    #    return redirect(url_for('search'))

    if category:
        query_dict['category'] = category

    if service:
        query_dict['service'] = service

    if parish:
        query_dict['parish'] = parish

    if area:
        query_dict['area'] = area

    if rating:
        query_dict['rating'] = rating

    recommendations = Recommendation.query.filter_by(**query_dict)

    query_list = []
    if name:
        name = name.split()
        for n in name:
            query_list.append(Recommendation.name.ilike("%"+n+"%"))
            query_list.append(Recommendation.category.ilike("%"+n+"%"))
            query_list.append(Recommendation.service.ilike("%"+n+"%"))

        recommendations = recommendations.filter(
            reduce(
                lambda a, b: (
                    a | b), query_list))







    try:
        page = int(request.args.get("page", '1'))
    except ValueError:
        page = 1

    #recommendations = recommendations.paginate(page,ITEMS_PER_PAGE,False)
    recommendations = recommendations.order_by(
        sqlalchemy.sql.expression.case(
            ((Recommendation.rating == "Excellent", 1),
             (Recommendation.rating == "Very Good", 2),
                (Recommendation.rating == "Average", 3),
                (Recommendation.rating == "Poor", 4),
                (Recommendation.rating == "Terrible", 5)))).paginate(
        page, ITEMS_PER_PAGE, False)

    return render_template(
        'search/mainsearch.html',
        title='Search',
        form=form,
        recommendations=recommendations,
        queries=urllib.urlencode(queries_without_page),
        btnclicked=True)


@app.route('/logout')
def logout():
    if g.user.is_authenticated():
        g.user.last_seen = datetime.now()
        db.session.add(g.user)
        db.session.commit()
    logout_user()
    flash('You have successfully logged out!', category='success')
    return redirect(url_for('login'))


@app.route('/user/profile')
@login_required
def user():
    user_email = g.user.email
    user = User.query.filter_by(email=user_email).first()
    if user is None:
        flash('User not found.', category='danger')
        return redirect(url_for('index'))
    return render_template('users/user.html',
                           user=user)


# TODO: YOW THIS WORKS PERFECTLY
@app.route('/friendsjs', methods=['GET', 'POST'])
def friendsJS():
    friends = Friend.query.all()
    if request_wants_json():
        return jsonify(friends=[x.to_json() for x in friends])
    return render_template('testjs/index.html', friends=friends)


@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    form = FriendForm()
    user = User.query.filter_by(id=g.user.id).first()
    friends = user.friends.order_by(Friend.firstname).all()
    ads = getAds()
    if form.validate_on_submit():
        f = Friend.query.filter_by(email=form.email.data).first()
        if f and f.owner.id == g.user.id:
            flash(
                'You already have a friend with this email!',
                category='danger')
            return redirect(url_for('friends'))
        friend = Friend(
            user_id=g.user.id,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data)
        db.session.add(friend)
        db.session.commit()
        flash("Your friend is now Created", category='success')
        return redirect(url_for('friends'))
    return render_template('friends/friends.html',
                           title='Friends',
                           form=form,
                           friends=friends,
                           ads=ads
                           )


@app.route('/deletefriend/<int:id>', methods=['GET', 'POST'])
@login_required
def deletefriend(id):
    friend = Friend.query.filter_by(id=int(id)).first()
    #friend = Friend.query.get(id=int(id))
    if friend.owner.id == g.user.id:
        db.session.delete(friend)
        db.session.commit()
        flash("Your friend is now deleted")
    return redirect(url_for('friends'))


@app.route('/deletemultiplefriends', methods=['GET', 'POST'])
@login_required
def deletemultiplefriends():
    friendlist = request.form.getlist('friends')
    if not friendlist:
        flash("You need to select at least one friend", category='info')
        return redirect(url_for('friends'))
    for f in friendlist:
        friend = Friend.query.filter_by(id=int(f)).first()
        if friend.owner.id == g.user.id:
            replies = ReplyRecommendation.query.filter_by(
                friendid=friend.id).all()
            for r in replies:
                db.session.delete(r)
                db.session.commit()
            sends = SendAsk.query.filter_by(friendid=friend.id).all()
            for s in sends:
                db.session.delete(s)
                db.session.commit()
            sends2 = SendRecommendation.query.filter_by(
                friendid=friend.id).all()
            for s2 in sends2:
                db.session.delete(s2)
                db.session.commit()
            db.session.delete(friend)
            db.session.commit()
    flash("You have deleted the selected friends", category='success')
    return redirect(url_for('friends'))


@app.route('/editrecommendation/<int:id>', methods=['GET', 'POST'])
@login_required
def editrecommendation(id):
    form = RecommendationForm()
    recommendation = Recommendation.query.filter_by(id=int(id)).first()
    if request.method == 'POST':
        if form.category.data:
            form.service.choices = getServiceList(form.category.data)

        if form.validate_on_submit() and recommendation.user_id == g.user.id:
            recommendation.category = form.category.data
            recommendation.service = form.service.data
            recommendation.name = form.name.data
            recommendation.company = form.company.data
            recommendation.phone = form.phone.data
            recommendation.email = form.email.data
            recommendation.website = form.website.data
            recommendation.parish = form.parish.data
            recommendation.area = form.area.data
            recommendation.rating = form.rating.data
            recommendation.review = form.review.data
            recommendation.created = datetime.now()
            db.session.add(recommendation)
            db.session.commit()

            flash('Your changes have been saved.', category='success')
            return redirect(url_for('recommendations'))

    form.service.choices = getServiceList(recommendation.category)
    form.category.data = recommendation.category
    form.service.data = recommendation.service
    form.name.data = recommendation.name
    form.company.data = recommendation.company
    form.phone.data = recommendation.phone
    form.email.data = recommendation.email
    form.website.data = recommendation.website
    form.parish.data = recommendation.parish
    form.area.data = recommendation.area
    form.rating.data = recommendation.rating
    form.review.data = recommendation.review
    return render_template('recommendations/editrecommendation.html', form=form)


@app.route('/deleterecommendation/<int:id>', methods=['GET', 'POST'])
@login_required
def deleterecommendation(id):
    recommendation = Recommendation.query.filter_by(id=int(id)).first()
    if recommendation.user_id == g.user.id:
        sends2 = ReplyRecommendation.query.filter_by(
            recommendationid=recommendation.id).all()
        for s2 in sends2:
            db.session.delete(s2)
            db.session.commit()
        sends3 = SendRecommendation.query.filter_by(
            recommendationid=recommendation.id).all()
        for s3 in sends3:
            db.session.delete(s3)
            db.session.commit()
        db.session.delete(recommendation)
        db.session.commit()
        flash("Your Recommendation is now deleted", category='success')
    return redirect(url_for('recommendations'))


@app.route('/editfriend/<int:id>', methods=['GET', 'POST'])
@login_required
def editfriend(id):
    form = FriendForm()
    friend = Friend.query.filter_by(id=int(id)).first()
    if form.validate_on_submit() and friend.owner.id == g.user.id:
        friend.firstname = form.firstname.data
        friend.lastname = form.lastname.data
        friend.email = form.email.data
        db.session.add(friend)
        db.session.commit()
        flash('Your changes have been saved.', category='success')
        return redirect(url_for('friends'))
    else:
        form.firstname.data = friend.firstname
        form.lastname.data = friend.lastname
        form.email.data = friend.email
    return render_template('friends/editFriend.html',
                           form=form,
                           id=id)


@app.route('/editad/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def editad(id):
    ad = Ads.query.get_or_404(int(id))
    mypic = ad.pic
    form = AdEditForm()
    if form.validate_on_submit():
        filename = ""
        file = request.files['pic']
        if file:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(uuid.uuid4())
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                ad.pic = filename
            else:
                flash(
                    'Only jpeg, jpg or png files are accepted',
                    category='danger')
                return redirect(url_for('editad', id=ad.id))
        ad.title = form.title.data
        ad.website = form.website.data
        ad.body = form.body.data
        ad.ad_start_date = form.ad_start_date.data
        ad.ad_end_date = form.ad_end_date.data
        db.session.add(ad)
        db.session.commit()
        flash('Your changes have been saved.', category='success')
        return redirect(url_for('listads'))
    else:
        form.title.data = ad.title
        form.website.data = ad.website
        form.body.data = ad.body
        form.ad_start_date.data = ad.ad_start_date
        form.ad_end_date.data = ad.ad_end_date
    return render_template('ads/editad.html', form=form, id=id, mypic=mypic)


@app.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if g.user.password is None or g.user.password == "" or g.user.password == 'NULL':
            flash(
                'You did not set an old password. If this is a facebook account, you should use the Forget your password link on the log in page!',
                category='danger')
            return redirect(url_for('index'))
        if check_password_hash(g.user.password, form.oldpassword.data):
            g.user.password = generate_password_hash(form.password.data)
            db.session.add(g.user)
            db.session.commit()
            flash('Your password was successfully reset!', category='success')
            return redirect(url_for('reset'))
        else:
            flash("Your old password is incorrect!", category='danger')
            return redirect(url_for('reset'))
    return render_template('users/reset.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edituser():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and form.email.data != g.user.email:
            flash(
                'Sorry but this email is already registered at DehSuh!',
                category='danger')
            return redirect(url_for('edituser'))
        g.user.firstname = form.firstname.data
        g.user.lastname = form.lastname.data
        g.user.email = form.email.data
        g.user.phone= form.phone.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.', category='success')
        g.user.email = form.email.data
        return redirect(url_for('edituser'))
    else:
        form.firstname.data = g.user.firstname
        form.lastname.data = g.user.lastname
        form.email.data = g.user.email
        form.phone.data = g.user.phone
    return render_template('users/edituser.html',
                           form=form)


@app.route('/advertise')
def advertise():
    mform = MainSearchForm()
    return render_template(
        'advertise.html',
        title='Advertise With Us',
        mform=mform)


@app.route('/about')
def about():
    mform = MainSearchForm()
    return render_template('about.html', title='About Us', mform=mform)


@app.route('/terms')
def terms():
    mform = MainSearchForm()
    return render_template(
        'terms.html',
        title='Terms and Conditions',
        mform=mform)


@app.route('/privacy')
def privacy():
    mform = MainSearchForm()
    return render_template(
        'privacy.html',
        title='Privacy and Policy',
        mform=mform)


@app.route('/gettingstarted')
def gettingstarted():
    mform = MainSearchForm()
    return render_template(
        'gettingstarted.html',
        title='Getting Started',
        mform=mform)


@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    mform = MainSearchForm()
    form = ContactUsForm()
    if form.validate_on_submit():
        contact = ContactUs(
            name=form.name.data,
            email=form.email.data,
            topic=form.topic.data,
            message=form.message.data)
        db.session.add(contact)
        db.session.commit()
        flash("Your message was sent successfully", category='success')
        return redirect(url_for('contactus'))
    return render_template(
        'users/contactus.html',
        title='Contact Us',
        form=form,
        mform=mform)


@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    mform = MainSearchForm()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('This email is not registered!', category='danger')
            return redirect(url_for('changepassword'))
        else:
            forgot_password_notification(user)
            flash('Instructions were sent to your email', category='info')
            return redirect(url_for('changepassword'))
    return render_template(
        'users/changepassword.html',
        title='Change Password',
        form=form,
        mform=mform)


@app.route('/forgot_password/<p>', methods=['GET', 'POST'])
def forgot_password(p):
    mform = MainSearchForm()
    form = ForgotPasswordForm()
    user = User.query.filter_by(confirmationid=p).first()
    if not user:
        abort(404)
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        user.confirmationid = str(uuid.uuid4())
        db.session.add(user)
        db.session.commit()
        flash(
            "Your password was successfully changed! You can now log in with your new password!",
            category='success')
        return redirect(url_for('login'))
    return render_template(
        'users/forgotpassword.html',
        title="Forgot My Password",
        form=form,
        user=user,
        mform=mform)


@app.route('/search', methods=['GET', 'POST'])
#@app.route('/search/<int:page>', methods=['GET','POST'])
@login_required
def search():
    ads = getAds()
    form = SearchForm()
    #category = form.category.data
    name = request.args.get("name")
    category = request.args.get("category")
    #service = form.service.data
    service = request.args.get("service")
    parish = request.args.get("parish")
    area = request.args.get("area")
    rating = request.args.get("rating")
    recommendedby = request.args.get("recommendedby")
    buttonclicked = request.args.get("mybtn")
    query_dict = dict()

    if not buttonclicked:
        return render_template(
            'search/search.html',
            title='Search',
            form=form,
            recommendations=[],
            ads=ads,
            queries=[],
            btnclicked=None)

    queries_without_page = request.args.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']

    # if not category or not service and request.args.get("btn") == "sendsearch":
    #    flash("Please enter at least the Category and Service!",category='danger')
    #    return redirect(url_for('search'))

    if category:
        query_dict['category'] = category

    if service:
        query_dict['service'] = service

    if parish:
        query_dict['parish'] = parish

    if area:
        query_dict['area'] = area

    if rating:
        query_dict['rating'] = rating

    recommendations = Recommendation.query.filter_by(**query_dict)
    query_list = []
    if name:
        name = name.split()
        for n in name:
            query_list.append(Recommendation.name.ilike("%"+n+"%"))
            query_list.append(Recommendation.category.ilike("%"+n+"%"))
            query_list.append(Recommendation.service.ilike("%"+n+"%"))

        recommendations = recommendations.filter(
            reduce(
                lambda a, b: (
                    a | b), query_list))




    if recommendedby == 'Friends':
        recids = []
        user = User.query.filter_by(id=g.user.id).first()
        friends = user.friends.all()
        if not friends:
            flash(
                'You need to have at least one friend to perform this search',
                category='info')
            return redirect(url_for('search'))
        for friend in friends:
            reply_recs = ReplyRecommendation.query.filter_by(
                friendid=friend.id).all()
            for reply_rec in reply_recs:
                recids.append(reply_rec.recommendationid)

        if recids:
            recommendations = recommendations.filter(
                Recommendation.id.in_(recids))
    #recommendations = recommendations.all()
    try:
        page = int(request.args.get("page", '1'))
    except ValueError:
        page = 1

    recommendations = recommendations.order_by(
        sqlalchemy.sql.expression.case(
            ((Recommendation.rating == "Excellent", 1),
             (Recommendation.rating == "Very Good", 2),
                (Recommendation.rating == "Average", 3),
                (Recommendation.rating == "Poor", 4),
                (Recommendation.rating == "Terrible", 5)))).paginate(
        page, ITEMS_PER_PAGE, False)

    return render_template(
        'search/search.html',
        title='Search',
        form=form,
        recommendations=recommendations,
        ads=ads,
        queries=urllib.urlencode(queries_without_page),
        btnclicked=True)


@app.route(
    '/viewrecommendation/<int:recommendationid>',
    methods=[
        'GET',
        'POST'])
def viewrecommendation(recommendationid):
    mform = MainSearchForm()
    form = ReviewForm()
    recommendation = Recommendation.query.filter_by(
        id=int(recommendationid)).first()
    reviews = Review.query.filter_by(
        rec_id=int(recommendationid)).order_by(
        Review.created).all()

    if not recommendation:
        flash(
            'Sorry, but this recommendation was deleted by the Creator!',
            category='danger')
        return redirect(url_for('login'))
    # if recommendation.user_id == 0:
    #    recommender = db.session.query(Recommendation,Friend).filter(Recommendation.id==recommendation.id,Recommendation.friend_id == Friend.id).first()
    #    if recommender:
    #        recommender = recommender.Friend
    # else:
    #    recommender = db.session.query(User,Recommendation).filter(User.id == Recommendation.user_id).first()
    #    recommender = recommender.User
    recommender = db.session.query(
        User,
        Recommendation).filter(
        Recommendation.id == recommendation.id,
        User.id == Recommendation.user_id).first()
    if recommender:
        recommender = recommender.User
    return render_template(
        'recommendations/viewrecommendation.html',
        title='View Recommendation',
        recommendation=recommendation,
        recommender=recommender,
        form=form,
        reviews=reviews,
        mform=mform)


@app.route(
    '/sendrecommendation2/<int:askid>/<int:friendid>',
    methods=[
        'GET',
        'POST'])
@login_required
def sendrecommendation2(askid, friendid):
    recList = []
    ask = Ask.query.filter_by(id=int(askid)).first()
    friend = Friend.query.filter_by(id=int(friendid)).first()
    if not ask or not friend:
        flash(
            'Sorry, but this item was deleted by the owner! Please contact the person that sent you this request!',
            category='danger')
        return redirect(url_for('login'))
    asker = User.query.filter_by(id=ask.user_id).first()
    recommendations = Recommendation.query.filter_by(
        user_id=g.user.id,
        service=ask.service,
        category=ask.category).all()
    recommendationlist = request.form.getlist('sendmyrecommendations')
    if not recommendationlist and request.form.get('btn') == 'send':
        flash(
            "You need to select at least one Recommendation",
            category='danger')
        return redirect(
            url_for(
                'sendrecommendation2',
                askid=ask.id,
                friendid=friend.id))
    if recommendationlist:
        for r in recommendationlist:
            recList.append(r)
            replyrecommendation = ReplyRecommendation(
                recommendationid=int(r),
                friendid=friend.id,
                askid=ask.id,
                datesent=datetime.now())
            db.session.add(replyrecommendation)
            db.session.commit()
        recommendation_notification2(friend, asker, ask, recList)
        flash('Your Recommendations were sent successfully', category='success')
        return redirect(url_for('recommendations'))
    return render_template('recommendations/sendrecommendation2.html',
                           title="Send Recommendations",
                           ask=ask,
                           friend=friend,
                           asker=asker,
                           recommendations=recommendations)


@app.route(
    '/recommendation/<int:askid>/<int:friendid>',
    methods=[
        'GET',
        'POST'])
def sendrecommendation(askid, friendid):
    form = RecommendationReplyForm()
    ask = Ask.query.filter_by(id=int(askid)).first()
    friend = Friend.query.filter_by(id=int(friendid)).first()
    if not ask or not friend:
        flash(
            'Sorry, but this item was deleted by the owner! Please contact the person that sent you this request!',
            category='danger')
        return redirect(url_for('login'))
    asker = User.query.filter_by(id=ask.user_id).first()
    # FIXME:This will not work as I do not have the @login decorator(try using
    # a hidden field in the form)
    rec_user = form.user_id.data
    # TODO:Remove rec_user as we don't want to get the user ID
    if not rec_user:
        rec_user = 0
    #myuser =  request.form['user_id']
    if form.validate_on_submit():
        recommendation = Recommendation(
            user_id=0,
            category=ask.category,
            service=ask.service,
            name=form.name.data,
            company=form.company.data,
            phone=form.phone.data,
            email=form.email.data,
            website=form.website.data,
            parish=ask.parish,
            area=ask.area,
            rating=form.rating.data,
            review=form.review.data,
            created=datetime.now(),
            friend_id=int(friendid))
        db.session.add(recommendation)
        db.session.commit()
        # recommendation_notification(friend,rec_user,ask)
        replyrecommendation = ReplyRecommendation(
            recommendationid=recommendation.id,
            friendid=friend.id,
            askid=ask.id,
            datesent=datetime.now())
        db.session.add(replyrecommendation)
        db.session.commit()
        recommendation_notification(friend, asker, ask, recommendation.id)
        flash(
            "Your Recommendation was successfully sent to  %s %s ! You can send another if you like. Or just close this page!" %
            (asker.firstname, asker.lastname), category='success')
        return redirect(
            url_for(
                'sendrecommendation',
                askid=ask.id,
                friendid=friend.id))
    return render_template("recommendations/recommendationreply.html",
                           title="Send Recommendation",
                           form=form,
                           ask=ask,
                           asker=asker, friend=friend)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/listads', methods=['GET', 'POST'])
@admin_required
@login_required
def listads():
    form = AdForm()
    ads = Ads.query.all()
    if form.validate_on_submit():
        filename = ""
        file = request.files['pic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid4()) + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Only jpeg, jpg or png files are accepted', category='danger')
            return redirect(url_for('listads'))
        ad = Ads(title=form.title.data, website=form.website.data, body=form.body.data, pic=filename,
                 ad_start_date=form.ad_start_date.data,
                 #ad_start_date=datetime.strptime(form.ad_start_date.data, '%Y-%m-%d %H:%M:%S'),
                 ad_end_date=form.ad_end_date.data,
                 #ad_end_date=datetime.strptime(form.ad_end_date.data, '%Y-%m-%d %H:%M:%S'),
                 user_id=g.user.id, created=datetime.now()
                 )
        db.session.add(ad)
        db.session.commit()
        flash('Your Ad was successfully Created', category='success')
        return redirect(url_for('listads'))
    return render_template("ads/listads.html", form=form, ads=ads)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/deletead/<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def deletead(id):
    ad = Ads.query.filter_by(id=int(id)).first()
    db.session.delete(ad)
    db.session.commit()
    flash("Your Ad is now deleted", category='success')
    return redirect(url_for('listads'))

#======================RECIPES============================










#======================EVENTS============================

#helper to process youtube video links
def getCode(uTubeCode):
    if not uTubeCode:
        return
    codeList = uTubeCode.split('/')
    if (len(codeList) == 1):
        return codeList[0]
    else:
        codeList = codeList[-1]
        return codeList


@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():

    user = User.query.filter_by(id=g.user.id).first()
    events = Event.query.filter_by(
        creator=user.id,
        active=ACTIVE_EVENT).order_by("created_date desc").all()
    #asks = user.asks.all()
    #asks = asks.query.filter_by(status=ACTIVE_ASK).all()
    ads = getAds()
    form = EventForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print "REached Here"
            filename = ""
            fileThumb = ""
            file = request.files['flyer']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(uuid.uuid4()) + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                fileThumb = THUMBER(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        filename))
                fileThumb = os.path.basename(fileThumb)
            else:
                flash(
                    'Only jpeg, jpg or png files are accepted',
                    category='danger')
                return redirect(url_for('events'))
            event = Event(
                title=form.title.data,
                event_category=form.event_category.data,
                description=form.description.data,
                event_start_date=form.event_start_date.data,
                event_end_date=form.event_end_date.data,
                venue=form.venue.data,
                address=form.address.data,
                parish=form.parish.data,
                flyer=filename,
                # FIXME: thumbname needs to be fixed to a function to do that
                thumbnail=fileThumb,
                youtube=getCode(form.youtube.data),
                created_date=datetime.now(),
                creator=g.user.id,
                active=ACTIVE_EVENT
            )
            db.session.add(event)
            db.session.commit()
            flash('Your event was successfully created', category='success')
            return redirect(url_for('events'))
    return render_template("events/events.html",
                           title='Events',
                           form=form,
                           events=events,
                           ads=ads)


@app.route('/deleteevent/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteevent(id):
    event = Event.query.filter_by(id=int(id)).first()
    if event.creator == g.user.id:
        db.session.delete(event)
        db.session.commit()
        flash("Your Event is now deleted", category='success')
        return redirect(url_for('events'))
    flash("There is a problem deleting this event", category='danger')
    return redirect(url_for('events'))


@app.route('/detail/<int:id>#posts', methods=['GET', 'POST'])
@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def detail(id):
    event = Event.query.get_or_404(int(id))
    user = User.query.filter_by(id=event.creator).first()
    comments = Comment.query.filter_by(event_id=int(id)).order_by(Comment.created.desc()).all()
    ads=getAds()
    form = CommentForm()
    if request.method =='POST':
        if form.validate_on_submit():
            comment = Comment(
                event_id=int(id),
                author = form.author.data,
                content = form.content.data,
                rating = form.rating.data,
                created = datetime.now()
            )
            db.session.add(comment)
            db.session.commit()
            num = event.comment_counting
            if not num:
                num = 0
            event.comment_counting =  1 + num
            db.session.add(event)
            db.session.commit()
            flash("Your comment was successfully posted.", category='success')
            #return redirect(url_for('detail', id=id))
            return redirect('detail/'+str(id)+'#posts',code=302)
        else:
            flash("Please correct the errors on the Post form. Thanks.", category='danger')

    return render_template("events/detail.html",
                           title='Detail',
                           event=event,
                           user=user,
                           form=form,
                           comments=comments,
                           ads=ads
                           )
@app.route('/editevent/<int:id>', methods=['GET', 'POST'])
@login_required
def editevent(id):
    event = Event.query.get_or_404(int(id))
    mypic = event.flyer
    form = EventEditForm()
    ads=getAds()
    if form.validate_on_submit():
        filename = ""
        fileThumb = ""
        file = request.files['flyer']
        if file:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(uuid.uuid4()) + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                event.flyer = filename
                fileThumb = THUMBER(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        filename))
                event.thumbnail = os.path.basename(fileThumb)
            else:
                flash(
                    'Only jpeg, jpg or png files are accepted',
                    category='danger')
                return redirect(url_for('editevent', id=event.id))
        event.title = form.title.data
        event.event_category = form.event_category.data
        event.description = form.description.data
        event.event_start_date = form.event_start_date.data
        event.event_end_date = form.event_end_date.data
        event.venue = form.venue.data
        event.address = form.address.data
        event.parish = form.parish.data
        event.youtube = getCode(form.youtube.data)
        event.created_date = datetime.now()
        db.session.add(event)
        db.session.commit()
        flash('Your changes have been saved.', category='success')
        return redirect(url_for('events'))
    else:
        form.title.data = event.title
        form.event_category.data = event.event_category
        form.description.data = event.description
        form.event_start_date.data = event.event_start_date
        form.event_end_date.data = event.event_end_date
        form.venue.data = event.venue
        form.address.data = event.address
        form.parish.data = event.parish
        form.youtube.data = event.youtube
    return render_template(
        'events/editevents.html',
        id=id,
        form=form,
        mypic=mypic,
        ads=ads)
        

@app.route('/eventsearch', methods=['GET', 'POST'])
def eventsearch():
    title = request.args.get("title")
    event_category = request.args.get("event_category")
    #service = form.service.data
    event_start_date = request.args.get("event_start_date")
    #print event_start_date
    parish = request.args.get("parish")
    query_dict = dict()
    ads=getAds()
    #if event_start_date:
        #print event_start_date
        #datetimeobject = datetime.strptime(event_start_date, '%Y-%m-%d %H:%M:%S')
        #year = datetimeobject.year
        #month = datetimeobject.month
        #day = datetimeobject.day
        #hour = datetimeobject.hour
        #minute = datetimeobject.minute
        #print minute

    queries_without_page = request.args.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']

    # if not category or not service and request.args.get("btn") == "sendsearch":
    #    flash("Please enter at least the Category and Service!",category='danger')
    #    return redirect(url_for('search'))

    if event_category:
        query_dict['event_category'] = event_category


    if parish:
        query_dict['parish'] = parish


    events = Event.query.filter_by(**query_dict)

    query_list = []
    if title:
        title = title.split()
        for t in title:
            query_list.append(Event.title.ilike("%"+t+"%"))
            query_list.append(Event.event_category.ilike("%"+t+"%"))

        events = events.filter(
            reduce(
                lambda a, b: (
                    a | b), query_list))

    try:
        page = int(request.args.get("page", '1'))
    except ValueError:
        page = 1

    if event_start_date:
        print event_start_date
        datetimeobject = datetime.strptime(event_start_date, '%Y-%m-%d %H:%M:%S')
        year = datetimeobject.year
        month = datetimeobject.month
        day = datetimeobject.day
        hour = datetimeobject.hour
        minute = datetimeobject.minute

        events = events.filter(
            extract('year',Event.event_start_date) == year,
            extract('month',Event.event_start_date) == month,
            extract('day',Event.event_start_date) == day,
            extract('hour',Event.event_start_date) == hour,
            extract('minute',Event.event_start_date) == minute,
        )


    events = events.paginate(page,ITEMS_PER_PAGE,False)

    return render_template(
        'search/eventresults.html',
        title='Event Search Results',
        events=events,
        ads=ads,
        queries=urllib.urlencode(queries_without_page)
    )


@app.route('/findevents/<string:decide>', methods=['GET', 'POST'])
def findevents(decide):
    if decide not in ['today','tomorrow','upcoming']:
        abort(404)
    #year, month, day  = time.localtime()[:3]
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day
    #year = request.args.get("year")
    #month = request.args.get("month")
    #day = request.args.get("day")
    tomorrow = today + timedelta(days=1)
    year2 = tomorrow.year
    month2 = tomorrow.month
    day2 =  tomorrow.day

    tomorrow = tomorrow.replace(hour=23, minute=59, second=59,microsecond=0)


    ads = getAds()
    queries_without_page = request.args.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']

    try:
        page = int(request.args.get("page", '1'))
    except ValueError:
        page = 1

    if (decide == 'today'):
        events = Event.query.filter(
            extract('year',Event.event_start_date) == year,
            extract('month',Event.event_start_date) == month,
            extract('day',Event.event_start_date) == day
        ).paginate(page,ITEMS_PER_PAGE,False)
    elif(decide == 'tomorrow'):
        events = Event.query.filter(
            extract('year',Event.event_start_date) == year2,
            extract('month',Event.event_start_date) == month2,
            extract('day',Event.event_start_date) == day2
        ).paginate(page,ITEMS_PER_PAGE,False)
    else:
        events = Event.query.filter(Event.event_start_date > tomorrow).paginate(
            page,ITEMS_PER_PAGE,False
        )

    return render_template(
        'search/findevents.html',
        title='Event Search Result',
        events = events,
        ads = ads,
        queries=urllib.urlencode(queries_without_page)
    )

@app.route('/eventlist', methods=['GET', 'POST'])
def eventlist():
    year = request.form["year"]
    month = request.form["month"]
    day = request.form["day"]


    events = Event.query.filter(
        extract('year',Event.event_start_date) == year,
        extract('month',Event.event_start_date) == month,
        extract('day',Event.event_start_date) == day
    ).all()

    return jsonify(events=[x.to_json() for x in events])

@app.route('/iseventlist', methods=['GET', 'POST'])
def iseventlist():
    year = int(request.form["year"])
    month = int(request.form["month"])
    day = int(request.form["day"])
    #print year
    #print month
    #print day
    month = month+1

    events = Event.query.filter(
        extract('year',Event.event_start_date) == year,
        extract('month',Event.event_start_date) == month,
        extract('day',Event.event_start_date) == day
    ).all()

    if events:
        return jsonify({'answer':'T'})
    else:
        return jsonify({'answer':'F'})

