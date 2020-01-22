from flask import (
    Blueprint, redirect, url_for,
    render_template)
from flask_login import login_required, current_user
from project.models import BlockList, User, Dialogue, Chat, DoesNotExist
from .forms import ReportForm
from project.mailer import send_mail


report_blueprint = Blueprint('report', __name__)


@report_blueprint.route('/block/<string:username>')
@login_required
def block(username):
    person = User.get(User.username == username)
    BlockList.get_or_create(blocker=current_user.id, blocked_person=person.id)
    try:
        d = Dialogue.get(((Dialogue.user1 == person.id) &
                            (Dialogue.user2 == current_user.id)) |
                           ((Dialogue.user1 == current_user.id) &
                            (Dialogue.user2 == person.id)))
        c = Chat.select().where(Chat.dialogue == d.id)
        for i in c:
            i.delete_instance()
        d.delete_instance()
    except DoesNotExist:
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@report_blueprint.route('/remove/<int:id>')
@login_required
def remove(id):
    person = BlockList.get(BlockList.blocked_person == id)
    person.delete_instance()
    return redirect(url_for('report.blocklist'))


@report_blueprint.route('/blocklist')
@login_required
def blocklist():
    block_list = BlockList.select().where(BlockList.blocker == current_user.id)
    return render_template('report/blocklist.html', block_list=block_list)


@report_blueprint.route('/report/<id>', methods=['GET', 'POST'])
@login_required
def report_user(id):
    user = User.get(User.id == id)
    form = ReportForm()
    if form.validate_on_submit():
        message = form.message.data
        subject = "Yestomeet - Alerte"
        html = render_template(
            'email/alerte.html', message=message,
            bad_user=user.email, alert_user=current_user.email)
        user = 'hamid_kawser@hotmail.be'
        send_mail(user, subject, html)
        return redirect(url_for('main.index'))
    return render_template(
        'report/alert-administrator.html', form=form, user=user)
