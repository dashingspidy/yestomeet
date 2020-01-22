from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from project.models import User, Dialogue, Chat, DoesNotExist, Profile

chat_blueprint = Blueprint('chat', __name__)


@chat_blueprint.route('/inbox')
@login_required
def inbox():
    try:
        s = Dialogue.select().where(Dialogue.user1 == current_user.id)
        r = Dialogue.select().where(Dialogue.user2 == current_user.id)
        u_list = [User.get(User.id == i.user2.id) for i in s]
        for i in r:
            u_list.append(User.get(User.id == i.user1.id))
    except DoesNotExist:
        u_list = None
    return render_template('chat/inbox.html', u_list=u_list)


@chat_blueprint.route('/dialogue/<string:sender>', methods=['GET', 'POST'])
@login_required
def dialogue(sender=None):
    dia = None
    chat = None

    sender_user = User.get(User.username == sender)
    receiver_user = User.get(User.username == current_user.username)
    users = User.raw('select * from user u, dialogue d '
                     'where u.id != %s '
                     'and u.id in (d.user1_id, d.user2_id) '
                     'and %s in (d.user1_id, d.user2_id);', receiver_user.id, receiver_user.id)

    try:
        dia = Dialogue.get(((Dialogue.user1 == sender_user.id) &
                            (Dialogue.user2 == receiver_user.id)) |
                           ((Dialogue.user1 == receiver_user.id) &
                            (Dialogue.user2 == sender_user.id)))
    except DoesNotExist:
        dia = None

    user_profile = Profile.get(Profile.user == sender_user.id)
    current_profile = Profile.get(Profile.user == receiver_user.id)

    if not dia:
        if user_profile.room == 'room2' or current_profile.room == 'room2':
            dia = Dialogue.create(user1=sender_user.id,
                                  user2=receiver_user.id,
                                  exchange=20)
        else:
            dia = Dialogue.create(user1=sender_user.id,
                                  user2=receiver_user.id)
    session['dia'] = dia.id

    chat = Chat.select().where(Chat.dialogue == dia.id)

    if Chat.select().where(Chat.receiver == current_user.id, Chat.was_read == 0).exists():
        query = Chat.update(was_read=True).where(Chat.receiver == current_user.id)
        query.execute()

    count = Chat.select().where(Chat.dialogue == dia.id).count();
    return render_template(
        'chat/dialogue.html',
        users=users, chat=chat, sender=sender, dia=dia, count=count)
