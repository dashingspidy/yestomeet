from peewee import *
from datetime import datetime
from flask_login import UserMixin
from project.config import ProductionConfig


database = MySQLDatabase(
    ProductionConfig.MYSQL_DB_NAME,
    host=ProductionConfig.MYSQL_DB_HOST,
    user=ProductionConfig.MYSQL_DB_USERNAME,
    passwd=ProductionConfig.MYSQL_DB_PASSWORD,
    charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = database


class User(UserMixin, BaseModel):
    id = PrimaryKeyField(null=False)
    username = CharField(null=False, unique=True, max_length=25, index=True)
    email = CharField(null=False, unique=True, index=True)
    password_digest = CharField(null=False)
    confirmed = BooleanField(default=False, null=True)
    reset_digest = CharField(null=True)
    remember_digest = CharField(null=True)
    admin = BooleanField(null=False, default=False)
    birthdate = DateField()
    location = CharField()
    gender = CharField()
    looking_for = CharField()
    online = BooleanField(default=False)
    age = IntegerField(null=False)
    notif = IntegerField(null=False, default=True)
    registered_on = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        order_by = ('-registered_on',)


class Profile(BaseModel):
    user = ForeignKeyField(
        User, primary_key=True, unique=True,
        on_delete='CASCADE', related_name='profile')
    room = TextField(null=False)
    gift = BooleanField(null=False, default=False)
    description = TextField(null=False)
    romantic = CharField()
    marriage = CharField()
    want_children = CharField()
    nationality = CharField()
    height = CharField()
    body_type = CharField()
    style = CharField()
    origin = CharField()
    eyes = CharField()
    hair = CharField()
    hair_length = CharField()
    weight = CharField()
    status = CharField()
    smoke = CharField()
    children = CharField()
    live = CharField()
    job = CharField()
    eat = CharField()
    pet = CharField()
    religion = CharField()
    speak1 = CharField()
    speak2 = CharField()
    speak3 = CharField()
    speak4 = CharField()
    education = CharField()
    income = CharField()
    slogan = TextField()
    first_meet = TextField()
    quality = TextField()
    defauts = TextField()
    dream = TextField()
    love = TextField()
    partner = TextField()
    loisir = TextField()
    friend = TextField()
    experience = TextField()
    boulot = TextField()
    animal = TextField()
    enfant = TextField()
    future = TextField()
    fierte = TextField()
    culture = TextField()
    malaise = TextField()
    sortie = TextField()
    voyage = TextField()
    addication = TextField()
    passion = TextField()


class Address(BaseModel):
    user = ForeignKeyField(
        User, null=False, primary_key=True,
        unique=True, related_name='address')
    name = CharField(null=False)
    street = CharField(null=False)
    postal_code = CharField(null=False)
    telephone = IntegerField(null=False)
    country = CharField(null=False)


class Photo(BaseModel):
    id = PrimaryKeyField(null=False)
    url = CharField()
    user = ForeignKeyField(
        User, related_name='photos', null=False)
    default = BooleanField(default=False)
    private = BooleanField(default=False)


class Plan(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(null=False)
    plan_id = CharField(null=False)
    amount = IntegerField(null=False)
    period = CharField(null=False)
    description = CharField(null=False)


class Subscription(BaseModel):
    id = PrimaryKeyField(null=False)
    stripe_customer_id = CharField(null=False, unique=True, index=True)
    stripe_subscription_id = CharField(null=False, unique=True, index=True)
    plan = CharField(null=False)
    expire_at = DateTimeField(null=False)
    status = CharField(null=False)
    user = ForeignKeyField(
        User, null=False, index=True, unique=True,
        related_name='subscription')


class Blog(BaseModel):
    id = PrimaryKeyField(null=False)
    title = CharField(null=False)
    post = TextField(null=False)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        order_by = ('-created_at',)


class Visit(BaseModel):
    visitor = ForeignKeyField(User, related_name='visitor')
    person = ForeignKeyField(User, related_name='person')
    read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        indexes = (
            (('visitor', 'person'), True),
        )
        order_by = ('-created_at',)


class Slider(BaseModel):
    id = PrimaryKeyField(null=False)
    post = CharField(null=False, index=True)


class BlockList(BaseModel):
    id = PrimaryKeyField(null=False)
    blocker = ForeignKeyField(User, null=False, related_name='blocker')
    blocked_person = ForeignKeyField(User, null=False, related_name='blocked')

    class Meta:
        indexes = (
            (('blocker', 'blocked_person'), True),
            (('blocked_person', 'blocker'), True)
        )


class Dialogue(BaseModel):
    id = PrimaryKeyField()
    user1 = ForeignKeyField(User, null=False, related_name="user1")
    user2 = ForeignKeyField(User, null=False, related_name="user2")
    exchange = IntegerField(null=True)

    class Meta:
        indexes = (
            (('user1', 'user2'), True),
            (('user2', 'user1'), True),
        )


class Chat(BaseModel):
    id = PrimaryKeyField()
    message = CharField(null=False)
    was_read = BooleanField(default=False)

    dialogue = ForeignKeyField(
        Dialogue, null=False, related_name="dialogue")
    sender = ForeignKeyField(User, null=False, related_name="sender")
    receiver = ForeignKeyField(User, null=False, related_name="receiver")


class Friend(BaseModel):
    id = PrimaryKeyField()
    friend1 = ForeignKeyField(User, null=False, related_name="friend1")
    friend2 = ForeignKeyField(User, null=False, related_name="friend2")

    class Meta:
        indexes = (
            (('friend1', 'friend2'), True),
            (('friend2', 'friend1'), True),
        )


def initialize():
    database.connect()
    database.create_tables(
        [User, Profile, Photo, Plan, Subscription, Blog, Visit, Slider, BlockList, Address, Dialogue, Chat, Friend],
        safe=True)
    database.close()
