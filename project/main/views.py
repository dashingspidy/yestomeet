from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
import stripe
from project.models import (
    User, Photo, Profile, Friend, Slider,
    DoesNotExist, Subscription, Blog, Visit, BlockList)
from project.profile.form_values import *
from .forms import SearchForm, ContactForm
from project.mailer import send_mail, visit_notif
from project.decorators import no_profile, blocked_user_filter


main_blueprint = Blueprint('main', __name__)
stripe.api_key = "sk_test_KrE8zCZNuf8NUNsgeBLBZwO2"


@main_blueprint.route('/')
def index():
    if current_user.is_authenticated:
        return user_list()
    try:
        slide = Slider.select()
        yesdirect = User.select(User, Profile)\
                        .join(Profile)\
                        .where(Profile.room == 'room1')\
                        .limit(3)
        yestaketime = User.select(User, profile)\
                          .join(Profile)\
                          .where(Profile.room == 'room2')\
                          .limit(3)
    except DoesNotExist:
        slide = None
        yesdirect = None
        yestaketime = None
    return render_template(
        'main/index.html', slide=slide, direct=yesdirect, taketime=yestaketime)


@main_blueprint.route('/about')
def about():
    return render_template('main/about.html')


@main_blueprint.route('/conditions')
def conditions():
    return render_template('main/conditions.html')


@main_blueprint.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.nom.data
        email = form.email.data
        message = form.message.data
        telephone = form.telephone.data

        subject = "Yestomeet - Contact"
        html = render_template(
            'email/contact.html', message=message,
            name=name, email=email, telephone=telephone)
        user = 'hamid_kawser@hotmail.be'
        send_mail(user, subject, html)
        return redirect(url_for('main.confirm'))
    return render_template('main/contact.html', form=form)


@main_blueprint.route('/confirm_contact')
def confirm():
    return render_template('main/confirm.html')


@main_blueprint.route('/users')
@login_required
def user_list():
    try:
        b = BlockList.select().where(BlockList.blocker == current_user.id)
        v = BlockList.select().where(BlockList.blocked_person == current_user.id)
        blist = [i.blocked_person.id for i in b]
        for p in v:
            blist.append(p.blocker.id)
        if not blist:
            users = User.select()\
                        .where(
                            User.gender == current_user.looking_for)
        else:
            users = User.select()\
                        .where(
                            User.gender == current_user.looking_for,
                            User.id.not_in(blist))
    except DoesNotExist:
        users = None
    return render_template('main/users.html', users=users)


@main_blueprint.route('/profile/<string:username>')
@login_required
@blocked_user_filter
def profile(username):
    try:
        user = User.select(User, Profile)\
                   .join(Profile).where(User.username == username).get()
        p = Profile.get(user=current_user.id)
        try:
            Visit.get(visitor=current_user.id, person=user.id)
        except DoesNotExist:
            Visit.create(visitor=current_user.id, person=user.id)
            if user.notif:
                visit_notif(
                    user.email, current_user.username,
                    user.username, p.slogan)
        friend = Friend.select().where((
            (Friend.friend1 == current_user.id) & (Friend.friend2 == user.id) |
            (Friend.friend1 == user.id) & (Friend.friend2 == current_user.id)))
        if friend.exists():
            photos = Photo.select().where(Photo.user == user.id)
        else:
            photos = Photo.select()\
                          .where(Photo.user == user.id, Photo.private == 0)

    except DoesNotExist:
        user = None
        photos = None
    return render_template(
        'main/profile.html', user=user, photos=photos,
        nationality=dict(nationalities),
        rom=dict(romantic), religion=dict(religion),
        mar=dict(marriage), chil=dict(children), body=dict(body_type),
        st=dict(style), status=dict(marriage_status),
        ori=dict(origin), eye=dict(eyes), hair=dict(hair),
        harle=dict(hair_length), so=dict(smoke),
        have_chil=dict(have_children), live=dict(live),
        job=dict(job), eat=dict(eat), pet=dict(pet),
        speak=dict(speak), edu=dict(education),
        income=dict(income))


@main_blueprint.route('/my_account')
@login_required
@no_profile
def my_account():
    sub = Subscription.select().where(Subscription.user == current_user.id)
    if sub.exists():
        sub = sub.get()
    else:
        sub = None
    user = User.get(User.id == current_user.id)
    gift = current_user.profile.get()
    address = current_user.address.exists()
    if address:
        address = address
    else:
        address = None
    return render_template(
        'main/my_account.html', sub=sub, user=user,
        profile=gift, address=address)


@main_blueprint.route('/blog')
def blog():
    posts = Blog.select().order_by(Blog.created_at.desc())
    if posts.exists():
        posts = posts
    else:
        posts = None
    return render_template('main/blog.html', posts=posts)


@main_blueprint.route('/blog/<int:id>')
def article(id):
    post = Blog.get(Blog.id == id)
    return render_template('main/article.html', post=post)


@main_blueprint.route('/visit')
@login_required
def visit():
    visit_list = Visit.select()\
                      .where(Visit.person == current_user.id)\
                      .order_by(Visit.created_at.desc())
    if visit_list.exists():
        visit_list = visit_list
    else:
        visit_list = None
    if Visit.select()\
            .where(Visit.person == current_user.id, Visit.read == 0).exists():
        query = Visit.update(read=True).where(Visit.person == current_user.id)
        query.execute()

    return render_template('main/visit.html', visit_list=visit_list)


@main_blueprint.route('/gift_items')
@login_required
def gift_items():
    receiver = request.args.get('user')
    user = User.get(User.id == receiver)
    return render_template('main/items.html', receiver=receiver, user=user)


@main_blueprint.route('/gift_charge', methods=['POST'])
def gift_charge():
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=request.form['amount'],
        currency='eur'
    )
    user = User.get(User.id == int(request.form['user']))
    return render_template('main/send.html', user=user)


@main_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        age_min = int(form.age_min.data)
        age_max = int(form.age_max.data)
        gender = form.gender.data

        users = User.select().where(User.age.between(age_min, age_max),
                                    User.gender == gender,
                                    User.id != current_user.id)
        return render_template(
            'main/users.html',
            users=users)
    return render_template('main/search.html', form=form)


@main_blueprint.route('/online_users')
def online_users():
    try:
        b = BlockList.select().where(BlockList.blocker == current_user.id)
        v = BlockList.select().where(BlockList.blocked_person == current_user.id)
        blist = [i.blocked_person.id for i in b]
        for p in v:
            blist.append(p.blocker.id)
        if not blist:
            users = User.select()\
                        .where(
                            User.gender == current_user.looking_for,
                            User.online == 1)
        else:
            users = User.select()\
                        .where(
                            User.gender == current_user.looking_for,
                            User.id.not_in(blist),
                            User.online == 1)
    except DoesNotExist:
        users = None
    return render_template(
        'main/users.html',
        users=users,
        dsc="Voici les utilisateurs actuellement en ligne.Envoyez vite un petit message à ceux qui vous font craquer.")


@main_blueprint.route('/yestaketime')
def yestaketime():
    try:
        b = BlockList.select().where(BlockList.blocker == current_user.id)
        v = BlockList.select().where(BlockList.blocked_person == current_user.id)
        blist = [i.blocked_person.id for i in b]
        for p in v:
            blist.append(p.blocker.id)
        if not blist:
            users = User.select()\
                        .join(Profile)\
                        .where(
                            Profile.room == 'room2')
        else:
            users = User.select()\
                        .join(Profile)\
                        .where(
                            Profile.room == 'room2',
                            User.id.not_in(blist))
    except DoesNotExist:
        users = None
    return render_template('main/users.html', users=users)


@main_blueprint.route('/yestobedirect')
def yestobedirect():
    try:
        b = BlockList.select().where(BlockList.blocker == current_user.id)
        v = BlockList.select().where(BlockList.blocked_person == current_user.id)
        blist = [i.blocked_person.id for i in b]
        for p in v:
            blist.append(p.blocker.id)
        if not blist:
            users = User.select()\
                        .join(Profile)\
                        .where(
                            Profile.room == 'room1')
        else:
            users = User.select()\
                        .join(Profile)\
                        .where(
                            Profile.room == 'room1',
                            User.id.not_in(blist))
    except DoesNotExist:
        users = None
    return render_template('main/users.html', users=users)
