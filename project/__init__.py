from gevent import monkey
monkey.patch_all()
from flask import Flask, redirect, url_for, render_template, g, request
from flask_login import LoginManager, current_user, login_required
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_babel import Babel
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_socketio import SocketIO
from project.config import ProductionConfig


app = Flask(__name__)
app.config.from_object('project.config.ProductionConfig')

socketio = SocketIO()
socketio.init_app(
    app,
    async_mode='gevent',
    message_queue='redis://yestomeetyou.fxwesb.0001.euc1.cache.amazonaws.com:6379')
admin = Admin(
    app,
    name="Yestomeet",
    template_mode='bootstrap3',
    url='/1a1fa5ef7e744ab9837f3c5244c1981e1a1fa5ef7e744ab9837f3c5244c1981e')
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
babel = Babel(app)


from project.main.views import main_blueprint
from project.user.views import user_blueprint
from project.profile.views import profile_blueprint
from project.subscription.views import subscription_blueprint
from project.report.views import report_blueprint
from project.chat.views import chat_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(subscription_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(chat_blueprint)


from project.models import *


login_manager.login_view = 'user.login'


class MyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin


admin.add_view(MyView(User, endpoint="Utilisateur"))
admin.add_view(MyView(Slider, endpoint="slide"))
admin.add_view(MyView(Profile, endpoint="profil"))
admin.add_view(MyView(Address, endpoint="adress"))
admin.add_view(MyView(Plan, endpoint="splan"))
admin.add_view(MyView(Blog, endpoint="blogger"))
admin.add_view(MyView(Photo, endpoint="images"))


@app.before_request
def before_request():
    g.db = database
    g.db.get_conn()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except DoesNotExist:
        return None


@app.context_processor
def counter():
    if current_user.is_authenticated:
        g.count = Visit.select()\
                       .where(Visit.person == current_user.id, Visit.read == 0)\
                       .count()
        return dict(count=g.count)
    else:
        return {}


@app.context_processor
def slider():
    slider = Slider.select()
    if slider.exists():
        g.messages = slider
        return dict(messages=g.messages)
    else:
        return {}


@app.context_processor
def unread_message_count():
    if current_user.is_authenticated:
        g.msg_count = Chat.select()\
            .where(Chat.receiver == current_user.id, Chat.was_read == 0)\
            .count()
        return dict(msg_count=g.msg_count)
    else:
        return {}
