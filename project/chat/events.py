from flask import session
from flask_socketio import emit, join_room
from flask_login import current_user
from project.models import Dialogue, Chat, User, Friend
from project.mailer import message_notif


from .. import socketio


@socketio.on('connect', namespace='/chat')
def connect():
    if current_user.is_authenticated:
        user = User.get(User.id == current_user.id)
        user.online = True
        user.save()


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    dia = session.get('dia')
    if dia:
        join_room(dia)
    # emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message"""
    dia = session.get('dia')
    emit('message', {'msg': current_user.username + ':' + message['msg']}, room=dia)

    sender_user_id = User.get(User.username == current_user.username).id
    dia = Dialogue.get(id=dia)
    if dia.user1.id == sender_user_id:
        receiver_user_id = dia.user2.id
    else:
        receiver_user_id = dia.user1.id

    Chat.create(dialogue=dia.id,
                message=message['msg'],
                sender=sender_user_id,
                receiver=receiver_user_id)
    if dia.exchange == 20:
        Friend.get_or_create(friend1=dia.user1,
                             friend2=dia.user2)
    u = User.get(id=receiver_user_id)
    if u.notif:
        message_notif(u.email, current_user.username, u.username, message['msg'])


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    if current_user.is_authenticated:
        user = User.get(User.id == current_user.id)
        user.online = False
        user.save()
