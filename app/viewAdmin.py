#from flask.ext.admin import Admin, BaseView, expose
from flask.ext.superadmin import Admin, model, BaseView,expose, AdminIndexView
from app import app, db, lm
from models import User, Ask, Friend, ContactUs, Recommendation, SendAsk, ReplyRecommendation,Ads
from flask.ext.login import current_user, login_required
from flask.ext.superadmin.contrib import sqlamodel

class MyModelView(model.ModelAdmin):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin()



# Create customized index view class
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin()


#admin
admin = Admin(app,'Auth',index_view=MyAdminIndexView())
#admin = Admin(app, 'Simple Models')

# Add view
admin.add_view(sqlamodel.ModelAdmin(User, session=db.session))
#admin.add_view(MyModelView(Friend, db.session))
#admin.add_view(MyModelView(Ask, db.session))


#admin.register(User, session=db.session)
admin.register(Ask, session=db.session)
admin.register(Friend, session=db.session)
admin.register(ContactUs, session=db.session)
admin.register(Recommendation, session=db.session)
admin.register(SendAsk, session=db.session)
admin.register(ReplyRecommendation, session=db.session)
admin.register(Ads, session=db.session)

#Adding a custom view
#admin.add_view(MyView(name="Yello"))
