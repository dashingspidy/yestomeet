from datetime import datetime
from flask import (
    Blueprint, render_template,
    redirect, request, url_for, flash)
from flask_login import current_user, login_required
import stripe

from project.models import Plan, Subscription

subscription_blueprint = Blueprint('subscription', __name__)
stripe.api_key = "sk_test_KrE8zCZNuf8NUNsgeBLBZwO2"


def convert_datetime(value):
    return datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')


@subscription_blueprint.route('/plans')
@login_required
def plan():
    plans = Plan.select()
    return render_template('subscription/plans.html', plans=plans)


@subscription_blueprint.route('/checkout')
def checkout():
    plan = request.args.get('plan')
    return render_template('subscription/checkout.html', plan=plan)


@subscription_blueprint.route('/charge', methods=['POST'])
@login_required
def charge():
    try:
        customer = stripe.Customer.create(
            email=current_user.email,
            source=request.form['stripeToken'],
            plan=request.form['plan'])
        flash("You are subscribed!")
    except Exception as a:
        print("An error occured {}".format(a))
    expire = convert_datetime(customer['subscriptions']['data'][0]['current_period_end'])
    if customer:
        Subscription.create(
            stripe_customer_id=customer.id,
            stripe_subscription_id=customer['subscriptions']['data'][0]['id'],
            plan=customer['subscriptions']['data'][0]['items']['data'][0]['plan']['id'],
            expire_at=expire,
            status=customer['subscriptions']['data'][0]['status'],
            user=current_user.id)
    return redirect(url_for('profile.profile'))


@subscription_blueprint.route('/cancel_subscription')
@login_required
def cancel_subscription():
    sub = Subscription.get(Subscription.user == current_user.id)
    st = stripe.Subscription.retrieve(sub.stripe_subscription_id)
    sc = stripe.Customer.retrieve(sub.stripe_customer_id)
    st.delete()
    sc.delete()
    sub.delete_instance()
    flash('Your subscription has been cancelled.')
    return redirect(url_for('main.my_account'))


@subscription_blueprint.route('/update_cc', methods=['POST'])
def update_cc():
    sub = Subscription.get(Subscription.user == current_user.id)
    sc = stripe.Customer.retrieve(sub.stripe_customer_id)
    sc.source = request.form['stripeToken']
    sc.save()
    flash('Your card has been updated!')
    return redirect(url_for('main.my_account'))
