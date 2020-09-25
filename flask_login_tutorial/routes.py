"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, jsonify, request, current_app, abort
from flask_login import current_user, login_required, logout_user
from .models import db, User, Wallet, Operation
import datetime

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.jinja2',
        title='Flask-Login Tutorial.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@main_bp.route('/api/wallet', methods=['GET'])
@login_required
def wallet():
    user_id = current_user.id
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if wallet is None:
        return jsonify({'error': 'wallet not exists for account'}), 403
    operations = Operation.query.filter_by(wallet_id=wallet.wallet_id).all()
    operations_list = [row.__dict__ for row in operations]
    for item in operations_list:
        del item['_sa_instance_state']

    return jsonify({'wallet_id': wallet.wallet_id, 'user_id': wallet.user_id, 'balance': wallet.balance, 'operations': operations_list})

@main_bp.route('/api/external_to_wallet', methods=['POST'])
@login_required
def external_to_wallet():
    # check bank account
    print('user: {}'.format(current_user.email))
    if current_app.config['BANK_EMAIL'] != current_user.email:
        return jsonify({'error': 'access denied, only bank account'}), 403

    # check amount
    amount = request.json.get('amount')
    if amount is None:
        return jsonify({'error': 'amount not exists'}), 403
    elif isinstance(amount, float) == False:
        return jsonify({'error': 'amount not Float'}), 403
    elif amount <= 0:
        return jsonify({'error': 'amount not positive'}), 403

    # check wallet
    wallet_id = request.json.get('wallet_id')
    wallet = Wallet.query.filter_by(wallet_id=wallet_id).first()
    print('send to wallet :{}'.format(wallet_id))
    if wallet is None:
        return jsonify({'error': 'wallet not exists'}), 403

    # create new operation and update wallet balance
    details = request.json.get('details', '')
    operation = Operation(
        wallet_id=wallet_id,
        amount=amount,
        details=details,
        timestamp=datetime.datetime.utcnow(),
        debet=False,
        opertype='external_in',
        contragent_id=0,
    )
    db.session.add(operation)
    db.session.commit()
    wallet.balance += amount
    db.session.commit()
    return jsonify({'status': 'OK', 'operation_id': operation.operation_id, 'wallet_id': wallet.wallet_id, 'balance': wallet.balance}), 200

@main_bp.route('/api/wallet_to_wallet', methods=['POST'])
@login_required
def wallet_to_wallet():
    user_id = current_user.id

    # check amount
    amount = request.json.get('amount')
    if amount is None:
        return jsonify({'error': 'amount not exists'}), 403
    elif isinstance(amount, float) == False:
        return jsonify({'error': 'amount not Float'}), 403
    elif amount <= 0:
        return jsonify({'error': 'amount not positive'}), 403

    # check receiver wallet
    receiver_wallet_id = request.json.get('wallet_id')
    receiver_wallet = Wallet.query.filter_by(wallet_id=receiver_wallet_id).first()
    if receiver_wallet is None:
        return jsonify({'error': 'receiver wallet not exists'}), 403
    elif receiver_wallet.user_id == user_id:
        return jsonify({'error': 'sender wallet is receiver wallet'}), 403

    # check sender wallet
    sender_wallet = Wallet.query.filter_by(user_id=user_id).first()
    if sender_wallet.balance<amount:
        return jsonify({'error': 'amount > balance on wallet'}), 403

    # create new operations and update wallets balances
    sender_wallet.balance -= amount
    db.session.commit()

    sender_operation = Operation(
        wallet_id=sender_wallet.wallet_id,
        amount=amount,
        details='отправлено {} на кошелек {}'.format(amount, receiver_wallet_id),
        timestamp=datetime.datetime.utcnow(),
        debet=True,
        opertype='w2w_onestep',
        contragent_id=receiver_wallet_id,
    )
    db.session.add(sender_operation)
    db.session.commit()

    receiver_operation = Operation(
        wallet_id=receiver_wallet.wallet_id,
        amount=amount,
        details='получено {} с кошелька {}'.format(amount, sender_wallet.wallet_id),
        timestamp=datetime.datetime.utcnow(),
        debet=False,
        opertype='w2w_onestep',
        contragent_id=sender_wallet.wallet_id,
    )
    db.session.add(receiver_operation)
    db.session.commit()

    receiver_wallet.balance += amount
    db.session.add(receiver_wallet)
    db.session.commit()

    return jsonify({'status': 'OK', 'operation_id': sender_operation.operation_id, 'wallet_id': sender_wallet.wallet_id, 'balance': sender_wallet.balance}), 200