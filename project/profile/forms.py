from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import (
    SelectField, TextAreaField, SelectMultipleField,
    TextField, RadioField)
from wtforms.validators import DataRequired, Length
from flask_babel import gettext
from .form_values import *


class ProfileForm(FlaskForm):
    gift = RadioField('Cadeau', coerce=int,
        choices=[(1, gettext('Oui')), (0, gettext('Non'))])
    room = SelectField(
        gettext('Choisissez une salle'),
        choices=[('room1', 'Yes To Be Direct'), ('room2', 'Yes To Take Time')])
    description = TextAreaField(
        gettext('Description'),
        validators=[DataRequired(), Length(min=2)],
        render_kw={"placeholder": gettext('Minimum 50 caractères')})
    romantic = SelectField(
        gettext('Romantique'),
        validators=[DataRequired()],
        choices=[item for item in romantic])
    marriage = SelectField(
        gettext('Pour moi le mariage c\'est'),
        validators=[DataRequired()],
        choices=[item for item in marriage])
    want_children = SelectField(
        gettext('Je veux des enfants'),
        validators=[DataRequired()],
        choices=[item for item in children])
    nationality = SelectField(
        gettext('Ma nationalité'),
        validators=[DataRequired()],
        choices=[item for item in nationalities])
    height = SelectField(
        gettext('Ma taille'),
        choices=[(f"{i} cm", f"{i} cm") for i in range(140, 201)])
    body_type = SelectField(
        gettext('Ma silhouette'),
        validators=[DataRequired()],
        choices=[item for item in body_type])
    style = SelectField(
        gettext('Mon style'),
        validators=[DataRequired()],
        choices=[item for item in style])
    origin = SelectField(
        gettext('Mon origine'),
        validators=[DataRequired()],
        choices=[item for item in origin])
    eyes = SelectField(
        gettext('Mes yeux'),
        validators=[DataRequired()],
        choices=[item for item in eyes])
    hair = SelectField(
        gettext('Mes cheveux'),
        validators=[DataRequired()],
        choices=[item for item in hair])
    hair_length = SelectField(
        gettext('Longueur de mes cheveux'),
        validators=[DataRequired()],
        choices=[item for item in hair_length])
    weight = SelectField(
        gettext('Mon poids'),
        choices=[(f"{i} kg", f"{i} kg") for i in range(30, 140)])
    status = SelectField(
        gettext('Mon statut marital'),
        validators=[DataRequired()],
        choices=[item for item in marriage_status])
    smoke = SelectField(
        gettext('Je fume'),
        validators=[DataRequired()],
        choices=[item for item in smoke])
    children = SelectField(
        gettext('J\'ai des enfants'),
        validators=[DataRequired()],
        choices=[item for item in have_children])
    live = SelectField(
        gettext('Je vis'),
        validators=[DataRequired()],
        choices=[item for item in live])
    job = SelectField(
        gettext('Ma profession'),
        validators=[DataRequired()],
        choices=[item for item in job])
    religion = SelectField(
        gettext('Ma religion'),
        validators=[DataRequired()],
        choices=[item for item in religion])
    eat = SelectField(
        gettext('Je mange'),
        validators=[DataRequired()],
        choices=[item for item in eat])
    pet = SelectField(
        gettext('Mes animaux de compagnie'),
        validators=[DataRequired()],
        choices=[item for item in pet])
    speak1 = SelectField(
        gettext('Je parle'),
        validators=[DataRequired()],
        choices=[item for item in speak])
    speak2 = SelectField(
        gettext('Je parle'),
        validators=[DataRequired()],
        choices=[item for item in speak])
    speak3 = SelectField(
        gettext('Je parle'),
        validators=[DataRequired()],
        choices=[item for item in speak])
    speak4 = SelectField(
        gettext('Je parle'),
        validators=[DataRequired()],
        choices=[item for item in speak])
    education = SelectField(
        gettext('Quelles études avez-vous faites?'),
        validators=[DataRequired()],
        choices=[item for item in education])
    income = SelectField(
        gettext('Mes revenus'),
        validators=[DataRequired()],
        choices=[item for item in income])
    slogan = TextAreaField(
        gettext('Votre slogan: Une devise, une citation, exprimez en une phrase votre personnalité.'),
        validators=[DataRequired(), Length(min=50)])
    first_meet = TextAreaField(
        gettext('Premier rendez-vous: Décrivez le premier rendez-vous parfait.'),
        validators=[DataRequired(), Length(min=50)])
    quality = TextAreaField(
        gettext('Qualités: Dites-nous vos points forts.'),
        validators=[DataRequired(), Length(min=50)])
    defauts = TextAreaField(
        gettext('Défauts: Que doit-on redouter chez vous ?'),
        validators=[DataRequired(), Length(min=50)])
    dream = TextAreaField(
        gettext('Rêves: Parlez-nous de vos aspirations.'),
        validators=[DataRequired(), Length(min=50)])
    love = TextAreaField(
        gettext('Amour: Comment définiriez-vous ce grand concept ?'),
        validators=[DataRequired(), Length(min=50)])
    partner = TextAreaField(
        gettext('Partenaire: Comment vous le/la voyez ?'),
        validators=[DataRequired(), Length(min=50)])
    loisir = TextAreaField(
        gettext('Loisirs: Comment occupez-vous vos temps libres ?'),
        validators=[DataRequired(), Length(min=50)])
    friend = TextAreaField(
        gettext('Amis: Ils sont importants pour vous ?'),
        validators=[DataRequired(), Length(min=50)])
    experience = TextAreaField(
        gettext('Expérience forte: Racontez un évènement qui vous a marqué.'),
        validators=[DataRequired(), Length(min=50)])
    boulot = TextAreaField(
        gettext('Boulot: Il occupe quelle place dans votre vie ?'),
        validators=[DataRequired(), Length(min=50)])
    animal = TextAreaField(
        gettext('Animaux: Pour vous, c’est un plus ou bof ?'))
    enfant = TextAreaField(
        gettext('Enfants: Pour vous, c’est une force ?'),
        validators=[DataRequired(), Length(min=50)])
    future = TextAreaField(
        gettext('Avenir: Vous vous voyez où dans 20 ans ? (Et avec qui ?)'),
        validators=[DataRequired(), Length(min=50)])
    fierte = TextAreaField(
        gettext('Fierté: Qu’est-ce qui vous fait briller en société ?'),
        validators=[DataRequired(), Length(min=50)])
    culture = TextAreaField(
        gettext('Culture: Vous y attachez de l’importance ?'),
        validators=[DataRequired(), Length(min=50)])
    malaise = TextAreaField(
        gettext('Malaise: Il doit bien y avoir un petit truc qui vous dérange dans la vie.'),
        validators=[DataRequired(), Length(min=50)])
    sortie = TextAreaField(
        gettext('Sorties: Qu’est-ce qui vous fait sortir de chez vous ?'),
        validators=[DataRequired(), Length(min=50)])
    voyage = TextAreaField(
        gettext('Voyages: Vous avez envie d’évasion en ce moment ? Quelles destinations vous attirent ?'),
        validators=[DataRequired(), Length(min=50)])
    addication = TextAreaField(
        gettext('Addictions: De quoi avez-vous du mal à vous passer ?'),
        validators=[DataRequired(), Length(min=50)])
    passion = TextAreaField(
        gettext('Passions: Qu’est-ce qui vous fait vibrer ?'),
        validators=[DataRequired(), Length(min=50)])
    photo = FileField(
        gettext('Ajouter un photo'),
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg'], gettext('Format: .jpeg, .jpg'))])


class ProfileUpdateForm(FlaskForm):
    gift = RadioField('Cadeau', coerce=int,
        choices=[(1, gettext('Oui')), (0, gettext('Non'))])
    room = SelectField(
        gettext('Choisissez Chambre'),
        choices=[('room1', 'Yes To Be Direct'), ('room2', 'Yes To Take Time')])
    description = TextAreaField(
        gettext('Description'), validators=[DataRequired(), Length(min=2)])
    romantic = SelectField(
        gettext('Romantique'),
        validators=[DataRequired()],
        choices=[item for item in romantic])
    marriage = SelectField(
        gettext('Pour moi le mariage c\'est'),
        validators=[DataRequired()],
        choices=[item for item in marriage])
    want_children = SelectField(
        gettext('Je veux des enfants'),
        validators=[DataRequired()],
        choices=[item for item in children])
    nationality = SelectField(
        gettext('Ma nationalité'),
        validators=[DataRequired()],
        choices=[item for item in nationalities])
    height = SelectField(
        gettext('Ma taille'),
        choices=[(f"{i} cm", f"{i} cm") for i in range(140, 201)])
    body_type = SelectField(
        gettext('Ma silhouette'),
        validators=[DataRequired()],
        choices=[item for item in body_type])
    style = SelectField(
        gettext('Mon style'),
        validators=[DataRequired()],
        choices=[item for item in style])
    origin = SelectField(
        gettext('Mon origine'),
        validators=[DataRequired()],
        choices=[item for item in origin])
    eyes = SelectField(
        gettext('Mes yeux'),
        validators=[DataRequired()],
        choices=[item for item in eyes])
    hair = SelectField(
        gettext('Mes cheveux'),
        validators=[DataRequired()],
        choices=[item for item in hair])
    hair_length = SelectField(
        gettext('Longueur de mes cheveux'),
        validators=[DataRequired()],
        choices=[item for item in hair_length])
    weight = SelectField(
        gettext('Mon poids'),
        choices=[(f"{i} kg", f"{i} kg") for i in range(30, 140)])
    status = SelectField(
        gettext('Mon statut marital'),
        validators=[DataRequired()],
        choices=[item for item in marriage_status])
    smoke = SelectField(
        gettext('Je fume'),
        validators=[DataRequired()],
        choices=[item for item in smoke])
    children = SelectField(
        gettext('J\'ai des enfants'),
        validators=[DataRequired()],
        choices=[item for item in have_children])
    live = SelectField(
        gettext('Je vis'),
        validators=[DataRequired()],
        choices=[item for item in live])
    job = SelectField(
        gettext('Ma profession'),
        validators=[DataRequired()],
        choices=[item for item in job])
    religion = SelectField(
        gettext('Ma religion'),
        validators=[DataRequired()],
        choices=[item for item in religion])
    eat = SelectField(
        gettext('Je mange'),
        validators=[DataRequired()],
        choices=[item for item in eat])
    pet = SelectField(
        gettext('Mes animaux de compagnie'),
        validators=[DataRequired()],
        choices=[item for item in pet])
    speak1 = SelectField(
        gettext('Je parle'),
        validators=[DataRequired()],
        choices=[item for item in speak])
    speak2 = SelectField(
        gettext('Je parle'),
        validators=[DataRequired()],
        choices=[item for item in speak])
    speak3 = SelectField(
        gettext('Je parle'),
        validators=[DataRequired()],
        choices=[item for item in speak])
    speak4 = SelectField(
        gettext('Je parle'),
        validators=[DataRequired()],
        choices=[item for item in speak])
    education = SelectField(
        gettext('Quelles études avez-vous faites?'),
        validators=[DataRequired()],
        choices=[item for item in education])
    income = SelectField(
        gettext('Mes revenus'),
        validators=[DataRequired()],
        choices=[item for item in income])
    slogan = TextAreaField(
        gettext('Votre slogan: Une devise, une citation, exprimez en une phrase votre personnalité.'),
        validators=[DataRequired(), Length(min=50)])
    first_meet = TextAreaField(
        gettext('Premier rendez-vous: Décrivez le premier rendez-vous parfait.'),
        validators=[DataRequired(), Length(min=50)])
    quality = TextAreaField(
        gettext('Qualités: Dites-nous vos points forts.'),
        validators=[DataRequired(), Length(min=50)])
    defauts = TextAreaField(
        gettext('Défauts: Que doit-on redouter chez vous ?'),
        validators=[DataRequired(), Length(min=50)])
    dream = TextAreaField(
        gettext('Rêves: Parlez-nous de vos aspirations.'),
        validators=[DataRequired(), Length(min=50)])
    love = TextAreaField(
        gettext('Amour: Comment définiriez-vous ce grand concept ?'),
        validators=[DataRequired(), Length(min=50)])
    partner = TextAreaField(
        gettext('Partenaire: Comment vous le/la voyez ?'),
        validators=[DataRequired(), Length(min=50)])
    loisir = TextAreaField(
        gettext('Loisirs: Comment occupez-vous vos temps libres ?'),
        validators=[DataRequired(), Length(min=50)])
    friend = TextAreaField(
        gettext('Amis: Ils sont importants pour vous ?'),
        validators=[DataRequired(), Length(min=50)])
    experience = TextAreaField(
        gettext('Expérience forte: Racontez un évènement qui vous a marqué.'),
        validators=[DataRequired(), Length(min=50)])
    boulot = TextAreaField(
        gettext('Boulot: Il occupe quelle place dans votre vie ?'),
        validators=[DataRequired(), Length(min=50)])
    animal = TextAreaField(
        gettext('Animaux: Pour vous, c’est un plus ou bof ?'))
    enfant = TextAreaField(
        gettext('Enfants: Pour vous, c’est une force ?'),
        validators=[DataRequired(), Length(min=50)])
    future = TextAreaField(
        gettext('Avenir: Vous vous voyez où dans 20 ans ? (Et avec qui ?)'),
        validators=[DataRequired(), Length(min=50)])
    fierte = TextAreaField(
        gettext('Fierté: Qu’est-ce qui vous fait briller en société ?'),
        validators=[DataRequired(), Length(min=50)])
    culture = TextAreaField(
        gettext('Culture: Vous y attachez de l’importance ?'),
        validators=[DataRequired(), Length(min=50)])
    malaise = TextAreaField(
        gettext('Malaise: Il doit bien y avoir un petit truc qui vous dérange dans la vie.'),
        validators=[DataRequired(), Length(min=50)])
    sortie = TextAreaField(
        gettext('Sorties: Qu’est-ce qui vous fait sortir de chez vous ?'),
        validators=[DataRequired(), Length(min=50)])
    voyage = TextAreaField(
        gettext('Voyages: Vous avez envie d’évasion en ce moment ? Quelles destinations vous attirent ?'),
        validators=[DataRequired(), Length(min=50)])
    addication = TextAreaField(
        gettext('Addictions: De quoi avez-vous du mal à vous passer ?'),
        validators=[DataRequired(), Length(min=50)])
    passion = TextAreaField(
        gettext('Passions: Qu’est-ce qui vous fait vibrer ?'),
        validators=[DataRequired(), Length(min=50)])


class UploadForm(FlaskForm):
    photo = FileField(
        gettext('Ajouter un photo'),
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg'], gettext('Format: .jpeg, .jpg'))])


class AddressForm(FlaskForm):
    name = TextField(
        gettext('Votre nom complet'), validators=[DataRequired()])
    street = TextField(
        gettext('Rue, N°'), validators=[DataRequired()])
    postal_code = TextField(
        gettext('Code postal'), validators=[DataRequired()])
    telephone = TextField(
        gettext('Téléphone'), validators=[DataRequired()])
    country = TextField(
        gettext('Pays'), validators=[DataRequired()])
