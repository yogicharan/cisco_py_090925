from repo import repo_sql_dict as repo

def menu():
    message = '''
Options are:
1 - Create Employee
2 - List All Employees
3 - Read Employee By Id
4 - Update Employee
5 - Delete Employee
6 - Exit 
Your Option:'''
    choice = int(input(message))
    if choice == 1:
        try:
            id = int(input('ID:'))
            name = input('Name:')
            age = int(input('Age:'))
            salary = float(input('Salary:'))
            is_active = (input('Active(y/n):').upper() == 'Y')

            employee = {'id':id, 'name':name, 'age':age, 
                        'salary':salary, 'is_active':is_active}
        
            repo.create_employee(employee)
            print('Employee Created Successfully.')
        except ValueError:
            print("Invalid input type. Please try again.")
        except repo.EmployeeAlreadyExistError as ex:
            print(f"{ex}")
        except repo.DatabaseError as ex:
            print(f"{ex}")
        
    elif choice == 2:
        try:
            print('List of Employees:')
            for employee in repo.read_all_employee():
                print(employee)
        except repo.DatabaseError as ex:
            print(f"{ex}")
    elif choice == 3:
        try:
            id = int(input('ID:'))
            employee = repo.read_by_id(id)
            if employee == None:
                print('Employee not found.')
            else:
                print(employee)
        except ValueError:
            print("Invalid ID format.")
        except repo.EmployeeNotFoundError as ex:
            print(f"{ex}")
        except repo.DatabaseError as ex:
            print(f"{ex}")
    elif choice == 4:
        try:
            id = int(input('ID:'))
            employee = repo.read_by_id(id)
            if employee == None: 
                print('Employee Not Found')
            else:
                print(employee)
                salary = float(input('New Salary:'))
                new_employee = {'id':employee['id'], 
                    'name':employee['name'], 
                    'age':employee['age'], 
                    'salary':salary, 
                    'is_active':employee['is_active']}
                repo.update(id, new_employee)
                print('Employee updated successfully.')
        except ValueError:
            print("Invalid ID format.")
        except repo.EmployeeNotFoundError as ex:
            print(f"{ex}")
        except repo.DatabaseError as ex:
            print(f"{ex}")
    elif choice == 5:
        try:
            id = int(input('ID:'))
            employee = repo.read_by_id(id)
            if employee == None: 
                print('Employee Not Found')
            else:
                repo.delete_employee(id)
                print('Employee Deleted Succesfully.')
        except ValueError:
            print("Invalid ID format.")
        except repo.EmployeeNotFoundError as ex:
            print(f"{ex}")
        except repo.DatabaseError as ex:
            print(f"{ex}")
    elif choice == 6: 
        print('Thank you for using Application')

    return choice 

def menus():
    choice = menu()
    while choice != 6:
        choice = menu()
    
menus()
