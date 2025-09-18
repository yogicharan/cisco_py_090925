from flask import Blueprint, request, current_app, jsonify
from .crud import create_account, get_account, list_accounts, update_account, delete_account
from .emailer import send_email_background
from .config import Config
from .exceptions import ValidationError

bp = Blueprint("bms", __name__)


@bp.route("/accounts", methods=["POST"])
def api_create_account():
    data = request.get_json() or {}
    name = data.get("name")
    number = data.get("number")
    balance = data.get("balance", 0.0)
    if not name or not number:
        raise ValidationError("name and number fields are required")
    account = create_account(name=name, number=number, balance=balance)

    # send email to owner in background
    config = Config.from_env()
    subject = f"New account created: {account.number}"
    body = f"Account {account.name} ({account.number}) created with balance {account.balance:.2f}."
    send_email_background(config, subject, config.OWNER_EMAIL, body)

    return jsonify(account.to_dict()), 201


@bp.route("/accounts/<int:account_id>", methods=["GET"])
def api_get_account(account_id):
    account = get_account(account_id)
    return jsonify(account.to_dict())


@bp.route("/accounts", methods=["GET"])
def api_list_accounts():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 100))
    accounts = list_accounts(offset=offset, limit=limit)
    return jsonify([a.to_dict() for a in accounts])


@bp.route("/accounts/<int:account_id>", methods=["PUT", "PATCH"])
def api_update_account(account_id):
    data = request.get_json() or {}
    allowed = {"name", "number", "balance"}
    updates = {k: data[k] for k in data.keys() & allowed}
    if not updates:
        raise ValidationError("No valid fields provided for update")
    account = update_account(account_id, **updates)
    return jsonify(account.to_dict())


@bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def api_delete_account(account_id):
    delete_account(account_id)
    return jsonify({"deleted": True})
