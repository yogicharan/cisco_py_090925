from db.db_setup import session, Employee 
from util.log import logging 
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db.exc import EmployeeNotFoundError, EmployeeAlreadyExistError, DatabaseError
#CRUD (Create, Read All | Read One, Update, Delete)
#Employee App - SQL DB - dict element

def create_employee(employee):
    try:
        employee_model = Employee(id = employee['id'],
            name = employee['name'],
            age = employee['age'],
            salary = employee['salary'],
            is_active = employee['is_active'] )
        session.add(employee_model) #INSERT stmt db 
        session.commit() 
        logging.info("employee created.")
    except IntegrityError as ex:
        session.rollback()
        logging.error("Duplicate employee id:%s",ex)
        raise EmployeeAlreadyExistError(f"Employee id={employee['id']} exists already.")
    except SQLAlchemyError as ex:
        session.rollback()
        logging.error("Database error in creating employee:%s",ex)
        raise DatabaseError("Error in creating employee.")
    
def read_all_employee():
    try:
        employees = session.query(Employee).all()
        dict_employees = []
        for employee in employees:
            employee_dict = {'id':employee.id, 
                'name':employee.name,
                'age':employee.age, 'salary':employee.salary,'is_active':employee.is_active}
            dict_employees.append(employee_dict)
        logging.info("read all employees.")
        return dict_employees 
    except SQLAlchemyError as ex:
        logging.error("Database error in reading all employees: %s", ex)
        raise DatabaseError("Error in reading employees.")
    
def read_model_by_id(id):
    try:
        employee = session.query(Employee).filter_by(id = id).first()
        logging.info("read employee model.")
        if not employee: #if employee == None:            
            raise EmployeeNotFoundError(f"Employee not found {id}.")
        return employee
    except SQLAlchemyError as ex:
        logging.error("Database error in reading employee model: %s", ex)
        raise DatabaseError("Error in reading employee model.")
    
def read_by_id(id):
    try:
        employee = read_model_by_id(id)
        if not employee: #if employee == None:
            logging.info(f"employee not found {id}.")
            return None
        employee_dict = {'id':employee.id,
            'name':employee.name,
            'age':employee.age,'salary':employee.salary,'is_active':employee.is_active} 
        logging.info("read employee for given id.")
        return employee_dict 
    except EmployeeNotFoundError as ex:
        raise
    except SQLAlchemyError as ex:
        logging.error("Database error in reading employee by id: %s", ex)
        raise DatabaseError("Error in reading employee by id.")
    
def update(id, new_employee):
    try:
        employee = read_model_by_id(id)        
        employee.salary = new_employee['salary']
        session.commit()
        logging.info("employee salary updated.")
    except EmployeeNotFoundError as ex:
        raise
    except SQLAlchemyError as ex:
        logging.error("Database error in updating employee: %s", ex)
        raise DatabaseError("Error in updating employee.")
    
def delete_employee(id):
    try:
        employee = read_model_by_id(id)    
        session.delete(employee)
        session.commit()
        logging.info("employee deleted.")
    except EmployeeNotFoundError as ex:
        raise
    except SQLAlchemyError as ex:
        logging.error("Database error in deleting employee: %s", ex)
        raise DatabaseError("Error in deleting employee.")


