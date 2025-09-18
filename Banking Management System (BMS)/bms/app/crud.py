"""

Provides CRUD (Create, Read, Update, Delete) operations for the Account model.
Implements database interactions using SQLAlchemy ORM for the
Banking Management System (BMS).

"""

from sqlalchemy.exc import IntegrityError
from .db import get_db
from .models import Account
from .exceptions import NotFoundError, ValidationError



def create_account(name: str, number: str, balance: float) -> Account:
    """
    Create a new account and persist it in the database.

    Args: name (str): Name of the account holder.
          number (str): Unique account number.
          balance (float): Initial account balance.

    Raises: ValidationError: If the account number is not unique.

    Returns: Account: The newly created Account object.
    """
    db = get_db()
    account = Account(name=name, number=number, balance=float(balance))
    db.add(account)
    try:
        db.commit()
        db.refresh(account)
    except IntegrityError:
        db.rollback()
        raise ValidationError(f"Account number must be unique: {number}")
    return account


def get_account(account_id: int) -> Account:
    """
        Retrieve an account by its ID.

        Args: account_id (int): Unique identifier of the account.

        Raises: NotFoundError: If no account exists with the given ID.

        Returns: Account: The Account object corresponding to the given ID.
    """
    db = get_db()
    acc = db.query(Account).filter(Account.id == account_id).first()
    if not acc:
        raise NotFoundError(f"Account id={account_id} not found")
    return acc


def list_accounts(offset: int = 0, limit: int = 100) -> list[Account]:
    """
        List accounts with optional pagination.

        Args:
            offset (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 100.

        Returns:
            list[Account]: A list of Account objects.
    """
    db = get_db()
    return db.query(Account).offset(offset).limit(limit).all()


def update_account(account_id: int, **fields) -> Account:
    """
    Update fields of an existing account.

    Args: account_id (int): ID of the account to update.
          **fields: Key-value pairs of attributes to update.

    Raises: NotFoundError: If the account does not exist.

    Returns: Account: The updated Account object.
    """
    db = get_db()
    acc = db.query(Account).filter(Account.id == account_id).first()
    if not acc:
        raise NotFoundError(f"Account id={account_id} not found")

    for k, v in fields.items():
        if hasattr(acc, k):
            setattr(acc, k, v)

    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc


def delete_account(account_id: int) -> bool:
    """
    Delete an account by its ID.

    Args: account_id (int): ID of the account to delete.

    Raises: NotFoundError: If the account does not exist.

    Returns: bool: True if the account was successfully deleted.
    """
    db = get_db()
    acc = db.query(Account).filter(Account.id == account_id).first()
    if not acc:
        raise NotFoundError(f"Account id={account_id} not found")

    db.delete(acc)
    db.commit()
    return True
