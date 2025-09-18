import pytest
from repo import repo_sql_dict as repo
from repo.repo_sql_dict import SQLAlchemyError, IntegrityError
from db.exc import EmployeeAlreadyExistError, DatabaseError
from db.db_setup import session, Employee

@pytest.fixture(autouse=True)
def clean_db():
    """Clean up Employee table before and after each test."""
    session.query(Employee).delete()
    session.commit()
    yield
    session.query(Employee).delete()
    session.commit()

# create_employee test cases
# 1 ✔️ `test_create_employee_success` → Verify an employee is inserted, and `read_by_id` returns correct dict.
def test_create_employee_success():
    employee_data = {
        "id": 1,
        "name": "Alice",
        "age": 30,
        "salary": 50000,
        "is_active": True,
    }

    # Act
    repo.create_employee(employee_data)
    result = repo.read_by_id(1)

    # Assert
    assert result is not None
    assert result["id"] == 1
    assert result["name"] == "Alice"
    assert result["salary"] == 50000

# 2 ✔️ `test_create_employee_duplicate_id` → Try inserting the same employee twice, assert `EmployeeAlreadyExistError` is raised.
def test_create_employee_duplicate_id():
    employee_data = {
        "id": 2,
        "name": "Bob",
        "age": 40,
        "salary": 60000,
        "is_active": True,
    }

    # First insert works
    repo.create_employee(employee_data)

    # Second insert with same ID should raise
    with pytest.raises(EmployeeAlreadyExistError):
        repo.create_employee(employee_data)

# 3 ✔️ `test_create_employee_db_error` → Mock `session.commit()` to raise `SQLAlchemyError`, assert `DatabaseError` is raised.
def test_create_employee_db_error(monkeypatch):
    employee_data = {
        "id": 3,
        "name": "Charlie",
        "age": 25,
        "salary": 45000,
        "is_active": False,
    }

    # Monkeypatch session.commit to throw SQLAlchemyError
    def bad_commit():
        raise DatabaseError("DB failure")

    monkeypatch.setattr(repo.session, "commit", bad_commit)

    with pytest.raises(DatabaseError):
        repo.create_employee(employee_data)

# read_all_employee test cases
# 1 ✔️ `test_read_all_employee_empty` → DB empty, expect empty list.
def test_read_all_employee_empty():
    # Act
    result = repo.read_all_employee()

    # Assert
    assert isinstance(result, list)
    assert result == []

# 2 ✔️ `test_read_all_employee_multiple` → Insert 2–3 employees, assert returned list matches inserted data.
def test_read_all_employee_multiple():
    employees = [
        {"id": 1, "name": "Alice", "age": 30, "salary": 50000, "is_active": True},
        {"id": 2, "name": "Bob", "age": 40, "salary": 60000, "is_active": False},
        {"id": 3, "name": "Charlie", "age": 25, "salary": 45000, "is_active": True},
    ]

    # Insert employees
    for emp in employees:
        repo.create_employee(emp)

    # Act
    result = repo.read_all_employee()

    # Assert
    assert isinstance(result, list)
    assert len(result) == 3

    # Convert to dict {id: name} for easier comparison
    result_map = {e["id"]: e["name"] for e in result}
    assert result_map[1] == "Alice"
    assert result_map[2] == "Bob"
    assert result_map[3] == "Charlie"


# read_by_id test cases
# 1 ✔️ `test_read_by_id_found` → Insert an employee, read by ID, assert dict matches.
def test_read_by_id_found():
    employee_data = {
        "id": 1,
        "name": "Alice",
        "age": 30,
        "salary": 50000,
        "is_active": True,
    }

    # Insert employee
    repo.create_employee(employee_data)

    # Act
    result = repo.read_by_id(1)

    # Assert
    assert result is not None
    assert result["id"] == 1
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["salary"] == 50000
    assert result["is_active"] is True

# 2 ✔️ `test_read_by_id_not_found` → Query with non-existing ID, assert returns `None`.
def test_read_by_id_not_found():
    # Act
    result = repo.read_by_id(999)  # non-existent employee

    # Assert
    assert result is None

# update test cases 
# 1 ✔️ `test_update_salary_success` → Insert employee, update salary, check DB reflects new salary.
def test_update_salary_success():
    employee_data = {
        "id": 1,
        "name": "Alice",
        "age": 30,
        "salary": 50000,
        "is_active": True,
    }

    # Insert employee
    repo.create_employee(employee_data)

    # Act → update salary
    new_data = {"salary": 75000}
    repo.update(1, new_data)

    # Assert → fetch again from DB
    updated = repo.read_by_id(1)
    assert updated is not None
    assert updated["salary"] == 75000
    assert updated["name"] == "Alice"  # unchanged

# 2 ✔️ `test_update_employee_not_found` → Update on non-existing ID, assert no exception, but nothing happens.
def test_update_employee_not_found():
    # Act → try to update non-existing employee
    new_data = {"salary": 90000}
    result = repo.update(999, new_data)

    # Assert → update returns None, nothing happens
    assert result is None
    assert repo.read_by_id(999) is None

# delete_employee test cases 
# 1 ✔️ `test_delete_employee_success` → Insert, delete, check `read_by_id` returns `None`.
def test_delete_employee_success():
    employee_data = {
        "id": 1,
        "name": "Alice",
        "age": 30,
        "salary": 50000,
        "is_active": True,
    }

    # Insert employee
    repo.create_employee(employee_data)
    assert repo.read_by_id(1) is not None  # sanity check

    # Act → delete employee
    repo.delete_employee(1)

    # Assert → employee should be gone
    assert repo.read_by_id(1) is None

# 2 ✔️ `test_delete_employee_not_found` → Delete with non-existing ID, assert no exception, but nothing happens.
def test_delete_employee_not_found():
    # Act → try deleting a non-existent employee
    result = repo.delete_employee(999)

    # Assert → function should return None, DB unchanged
    assert result is None
    assert repo.read_by_id(999) is None

# logging_on
# 1 ✔️ `test_logging_on_create_success` → Patch `logging.info` and assert it was called.
def test_logging_on_create_success(caplog):
    employee_data = {
        "id": 1,
        "name": "Alice",
        "age": 30,
        "salary": 50000,
        "is_active": True,
    }

    with caplog.at_level("INFO"):
        repo.create_employee(employee_data)

    # Assert → logging contains success message
    assert any("employee created." in message for message in caplog.messages)

# 2 ✔️ `test_logging_on_duplicate_employee` → Patch `logging.error` and assert it logs duplicate error.
def test_logging_on_duplicate_employee(caplog):
    employee_data = {
        "id": 2,
        "name": "Bob",
        "age": 40,
        "salary": 60000,
        "is_active": True,
    }

    repo.create_employee(employee_data)

    with caplog.at_level("ERROR"):
        with pytest.raises(EmployeeAlreadyExistError):
            repo.create_employee(employee_data)

    # Assert → logging contains duplicate error
    assert any("Duplicate employee id" in message for message in caplog.messages)

# advanced scenarioss

# 1 ✔️ `Transaction rollback check` → After failed `create_employee`, assert `session.rollback` was called.
def test_transaction_rollback_on_failure(monkeypatch):
    """Ensure rollback is called when commit fails."""
    employee_data = {
        "id": 1,
        "name": "Alice",
        "age": 30,
        "salary": 50000,
        "is_active": True,
    }

    called = {"rollback": False}

    # Monkeypatch rollback and commit
    def bad_commit():
        raise SQLAlchemyError("Simulated failure")

    def mock_rollback():
        called["rollback"] = True

    monkeypatch.setattr(repo.session, "commit", bad_commit)
    monkeypatch.setattr(repo.session, "rollback", mock_rollback)

    with pytest.raises(DatabaseError):
        repo.create_employee(employee_data)

    assert called["rollback"] is True

# 2 ✔️ `Boundary values` → Test `age=0`, `salary=0`, or `is_active=False`.
def test_create_employee_with_boundary_values():
    """Test boundary values like age=0, salary=0, is_active=False."""
    employee_data = {
        "id": 2,
        "name": "BoundaryCase",
        "age": 0,
        "salary": 0,
        "is_active": False,
    }

    repo.create_employee(employee_data)
    result = repo.read_by_id(2)

    assert result["age"] == 0
    assert result["salary"] == 0
    assert result["is_active"] is False

# 3 ✔️ `Concurrency simulation` → Two inserts with same ID in quick succession (if DB supports).
def test_concurrent_insert_same_id():
    """Simulate two inserts with the same ID back-to-back."""
    employee_data = {
        "id": 3,
        "name": "FirstInsert",
        "age": 28,
        "salary": 40000,
        "is_active": True,
    }

    # First insert succeeds
    repo.create_employee(employee_data)

    # Modify name but keep same ID
    employee_data2 = {
        "id": 3,
        "name": "SecondInsert",
        "age": 29,
        "salary": 45000,
        "is_active": True,
    }

    with pytest.raises(EmployeeAlreadyExistError):
        repo.create_employee(employee_data2)

    # Ensure DB still has the first insert
    result = repo.read_by_id(3)
    assert result["name"] == "FirstInsert"
    assert result["salary"] == 40000
