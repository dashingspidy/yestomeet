from uuid import uuid4
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from project.models import (
    Profile, Photo, database,
    IntegrityError, DoesNotExist, Address)
from .forms import (
    ProfileForm, UploadForm, AddressForm, ProfileUpdateForm)
from .helpers import upload_file_to_s3, delete_file_from_s3
from .form_values import *
from project.decorators import no_profile, profile_exist


profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/new_profile', methods=['GET', 'POST'])
@login_required
# @profile_exist
def new_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        try:
            with database.transaction():
                Profile.create(
                    user=current_user._get_current_object(),
                    room=form.room.data,
                    gift=form.gift.data,
                    description=form.description.data,
                    romantic=form.romantic.data,
                    marriage=form.marriage.data,
                    want_children=form.want_children.data,
                    nationality=form.nationality.data,
                    height=form.height.data,
                    body_type=form.body_type.data,
                    style=form.style.data,
                    origin=form.origin.data,
                    eyes=form.eyes.data,
                    hair=form.hair.data,
                    hair_length=form.hair_length.data,
                    weight=form.weight.data,
                    status=form.status.data,
                    smoke=form.smoke.data,
                    children=form.children.data,
                    live=form.live.data,
                    job=form.job.data,
                    eat=form.eat.data,
                    pet=form.pet.data,
                    speak1=form.speak1.data,
                    speak2=form.speak2.data,
                    speak3=form.speak3.data,
                    speak4=form.speak4.data,
                    education=form.education.data,
                    religion=form.religion.data,
                    income=form.income.data,
                    slogan=form.slogan.data,
                    first_meet=form.first_meet.data,
                    quality=form.quality.data,
                    defauts=form.defauts.data,
                    dream=form.dream.data,
                    love=form.love.data,
                    partner=form.partner.data,
                    loisir=form.loisir.data,
                    friend=form.friend.data,
                    experience=form.experience.data,
                    boulot=form.experience.data,
                    animal=form.animal.data,
                    enfant=form.enfant.data,
                    future=form.future.data,
                    fierte=form.fierte.data,
                    culture=form.culture.data,
                    malaise=form.malaise.data,
                    sortie=form.sortie.data,
                    voyage=form.voyage.data,
                    addication=form.addication.data,
                    passion=form.passion.data
                )
                photo = form.photo.data
                generated_name = uuid4().hex
                photo.filename = secure_filename(generated_name + photo.filename)
                output = upload_file_to_s3(
                    photo,
                    'yestomeetyou')
                p = Photo(
                    url=str(output),
                    user=current_user._get_current_object(),
                    default=True)
                if form.room.data == 'room2':
                    p.private = True
                    p.save()
                if form.gift.data == 1:
                    return redirect(url_for('profile.address'))
                return redirect(url_for('profile.profile'))
        except IntegrityError:
            flash('Unable to create profile', 'danger')

    return render_template('profile/new-profile.html', form=form)


@profile_blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile = Profile.get(Profile.user == current_user.id)
    form = ProfileUpdateForm(obj=profile)
    if form.validate_on_submit():
        try:
            with database.transaction():
                p = Profile(
                    user=current_user._get_current_object(),
                    gift=form.gift.data,
                    room=form.room.data,
                    description=form.description.data,
                    romantic=form.romantic.data,
                    marriage=form.marriage.data,
                    want_children=form.want_children.data,
                    nationality=form.nationality.data,
                    height=form.height.data,
                    body_type=form.body_type.data,
                    style=form.style.data,
                    origin=form.origin.data,
                    eyes=form.eyes.data,
                    hair=form.hair.data,
                    hair_length=form.hair_length.data,
                    weight=form.weight.data,
                    status=form.status.data,
                    smoke=form.smoke.data,
                    children=form.children.data,
                    live=form.live.data,
                    job=form.job.data,
                    eat=form.eat.data,
                    pet=form.pet.data,
                    speak1=form.speak1.data,
                    speak2=form.speak2.data,
                    speak3=form.speak3.data,
                    speak4=form.speak4.data,
                    education=form.education.data,
                    religion=form.religion.data,
                    income=form.income.data,
                    slogan=form.slogan.data,
                    first_meet=form.first_meet.data,
                    quality=form.quality.data,
                    defauts=form.defauts.data,
                    dream=form.dream.data,
                    love=form.love.data,
                    partner=form.partner.data,
                    loisir=form.loisir.data,
                    friend=form.friend.data,
                    experience=form.experience.data,
                    boulot=form.experience.data,
                    animal=form.animal.data,
                    enfant=form.enfant.data,
                    future=form.future.data,
                    fierte=form.fierte.data,
                    culture=form.culture.data,
                    malaise=form.malaise.data,
                    sortie=form.sortie.data,
                    voyage=form.voyage.data,
                    addication=form.addication.data,
                    passion=form.passion.data
                )
                p.save()
                if form.room.data == 'room1':
                    photo = Photo.select().where(Photo.user == current_user.id)
                    for p in photo:
                        p.private = False
                        p.save()
                flash('Your profile has been updated!')
                return redirect(url_for('profile.profile'))
        except IntegrityError:
            flash('Unable to create profile', 'danger')

    return render_template('profile/edit-profile.html', form=form)


@profile_blueprint.route('/profile')
@login_required
@no_profile
def profile():
    profile = Profile.get(Profile.user == current_user.id)
    try:
        photo = Photo.select()\
                     .where(Photo.user == current_user.id, Photo.default == 1)\
                     .get()
        photos = Photo.select().where(Photo.user == current_user.id)
    except DoesNotExist:
        photo = None
        photos = None
    return render_template(
        'profile/profile.html',
        profile=profile, nationality=dict(nationalities),
        rom=dict(romantic), religion=dict(religion),
        mar=dict(marriage), chil=dict(children), body=dict(body_type),
        st=dict(style), status=dict(marriage_status),
        ori=dict(origin), eye=dict(eyes), hair=dict(hair),
        harle=dict(hair_length), so=dict(smoke),
        have_chil=dict(have_children), live=dict(live),
        job=dict(job), eat=dict(eat), pet=dict(pet),
        speak=dict(speak), edu=dict(education),
        income=dict(income), photo=photo, photos=photos)


def get_room():
    p = Profile.get(Profile.user == current_user.id)
    return p.room == 'room2'


@profile_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        photo = form.photo.data
        generated_name = uuid4().hex
        photo.filename = secure_filename(generated_name + photo.filename)
        output = upload_file_to_s3(
            photo,
            'yestomeetyou')
        p = Photo(
            url=str(output),
            user=current_user._get_current_object())
        if get_room():
            p.private = True
        p.save()
    try:
        photo = Photo.select().where(Photo.user == current_user.id)
    except DoesNotExist:
        photo = None
    return render_template('profile/upload.html', form=form, photo=photo)


@profile_blueprint.route('/delete_pic/<int:id>')
@login_required
def delete_pic(id):
    p = Photo.get(Photo.id == id)
    delete_file_from_s3('yestomeetyou', '{}'.format(p.url))
    p.delete_instance()
    return redirect(url_for('profile.upload'))


@profile_blueprint.route('/pic_set/<int:id>')
@login_required
def set_profile_pic(id):
    pro = Photo.get(Photo.id == id)
    try:
        pic = Photo.select()\
                   .where(Photo.user == current_user.id, Photo.default == 1)\
                   .get()
        if pic.default:
            pic.default = False
            pic.save()
            pro.default = True
            pro.save()
    except DoesNotExist:
        pro.default = True
        pro.save()
    return redirect(url_for('profile.upload'))


@profile_blueprint.route('/add_address', methods=['GET', 'POST'])
@login_required
def address():
    form = AddressForm()
    if form.validate_on_submit():
        try:
            with database.transaction():
                Address.create(
                    user=current_user._get_current_object(),
                    name=form.name.data,
                    street=form.street.data,
                    postal_code=form.postal_code.data,
                    telephone=form.telephone.data,
                    country=form.country.data
                )
                flash('Your address has been successfully added.')
                return redirect(url_for('profile.profile'))
        except IntegrityError:
            flash('Something went wrong. Please try again or contact us.')
    return render_template('profile/address.html', form=form)


@profile_blueprint.route('/update_address', methods=['GET', 'POST'])
@login_required
def update_address():
    address = Address.get(Address.user == current_user.id)
    form = AddressForm(obj=address)
    if form.validate_on_submit():
        try:
            with database.transaction():
                a = Address(
                    user=current_user._get_current_object(),
                    name=form.name.data,
                    street=form.street.data,
                    postal_code=form.postal_code.data,
                    telephone=form.telephone.data,
                    country=form.country.data
                )
                a.save()
                flash('Your address has been successfully updated.')
                return redirect(url_for('profile.profile'))
        except IntegrityError:
            flash('Something went wrong. Please try again or contact us.')
    return render_template('profile/address.html', form=form)


@profile_blueprint.route('/update_gift')
def update_gift():
    u = current_user.profile.get()
    if u.gift == 1:
        u.gift = 0
        u.save()
    else:
        u.gift = 1
        u.save()
        try:
            current_user.address.get()
        except DoesNotExist:
            flash('Please add your address to receive gift.')
            return redirect(url_for('profile.address'))
    return redirect(url_for('main.my_account'))
