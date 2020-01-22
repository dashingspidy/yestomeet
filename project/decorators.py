from functools import wraps
from project import redirect, url_for
from .models import BlockList, User
from flask_login import current_user


def current_user_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not current_user:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return inner


def no_profile(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not current_user.profile:
            return redirect(url_for('profile.new_profile'))
        return f(*args, **kwargs)
    return inner


def profile_exist(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if current_user.profile:
            return redirect(url_for('profile.edit_profile'))
        return f(*args, **kwargs)
    return inner


def blocked_user_filter(f):
    @wraps(f)
    def inner(*args, **kwargs):
        username = kwargs['username']
        user = User.get(User.username == username)
        b = BlockList.select().where(BlockList.blocker == current_user.id)
        v = BlockList.select().where(BlockList.blocked_person == current_user.id)
        blist = [i.blocked_person.id for i in b]
        for p in v:
            blist.append(p.blocker.id)
        if user.id in blist:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return inner
