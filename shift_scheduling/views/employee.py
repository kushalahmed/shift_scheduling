import json
import logging

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_defaults, view_config

from shift_scheduling import Session
from shift_scheduling.views import BaseView
from shift_scheduling.models import Employee, Role, UnavailableDay


@view_defaults(route_name='employee', permission=NO_PERMISSION_REQUIRED, renderer="json")
class EmployeeView(BaseView):

    @view_config(request_method='POST')
    def post_employee(self):

        response = {
            'status': False,
            'error': None
        }

        body = json.loads(self.request.body.decode('utf-8'))

        firstname = None
        if 'firstname' in body:
            firstname = body['firstname']

        lastname = None
        if 'lastname' in body:
            lastname = body['lastname']

        maxhours = 0
        if 'maxhours' in body:
            maxhours = body['maxhours']

        roles = []
        if 'roles' in body:
            roles = body['roles']

        unavailable_days = []
        if 'unavailable_days' in body:
            unavailable_days = body['unavailable_days']

        try:
            # Add employee entry
            session = Session()
            employee = Employee(firstname=firstname, lastname=lastname, maxhours=maxhours)
            session.add(employee)

            # Add employee role entry
            for rolename in roles:
                employee_role = Role(rolename=rolename, employee=employee)
                session.add(employee_role)

            # Add unavailable day entry
            for unavailable_day in unavailable_days:
                employee_unavailable_day = UnavailableDay(weekday=unavailable_day, employee=employee)
                session.add(employee_unavailable_day)

            session.commit()

            response['status'] = True
            response['employee_id'] = employee.id

        except Exception as e:
            session.rollback()
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Employee's profile could not be created."
            return response

        finally:
            session.close()

        return response

    @view_config(request_method='GET')
    def get_employee(self):

        response = {
            'status': False,
            'error': None
        }

        if 'employee_id' in self.request.GET:
            employee_id = self.request.GET.get('employee_id')
        else:
            response['status'] = False
            response['error'] = "The 'employee_id's value is missing."
            return response

        try:

            session = Session()
            employee = session.query(Employee).filter_by(id=int(employee_id)).first()

        except Exception as e:
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Employee's profile could not be read."
            return response

        if employee is None:
            response['status'] = False
            response['error'] = "Employee's profile does not exist."
            return response

        try:
            roles = session.query(Role).filter_by(employee_id=employee.id).all()
            unavailable_days = session.query(UnavailableDay).filter_by(employee_id=employee.id).all()
        except Exception as e:
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Employee's information could not be fetched."
            return response

        response = {
            "status": True,
            "error": None,
            "firstname": employee.firstname,
            "lastname": employee.lastname,
            "roles": [],
            "maxhours": employee.maxhours,
            "unavailable_days": []
        }

        for role in roles:
            response['roles'].append(role.rolename)

        for unavailable_day in unavailable_days:
            response['unavailable_days'].append(unavailable_day.weekday)

        return response

    @view_config(request_method=["PUT", "UPDATE"])
    def update_employee(self):

        response = {
            'status': False,
            'error': None
        }

        body = json.loads(self.request.body.decode('utf-8'))

        if 'employee_id' in body:
            employee_id = body['employee_id']
        else:
            response['status'] = False
            response['error'] = "The 'employee_id's value is missing."
            return response

        try:
            session = Session()
            employee = session.query(Employee).filter_by(id=employee_id).first()

            if employee is None:
                response['status'] = False
                response['error'] = "Employee's profile does not exist."
                return response

            if 'firstname' in body:
                employee.firstname = body['firstname']

            if 'lastname' in body:
                employee.lastname = body['lastname']

            if 'maxhours' in body:
                employee.maxhours = body['maxhours']

            if 'roles' in body:
                session.query(Role).filter_by(employee_id=employee_id).delete()
                for rolename in body['roles']:
                    employee_role = Role(rolename=rolename, employee=employee)
                    session.add(employee_role)

            if 'unavailable_days' in body:
                session.query(UnavailableDay).filter_by(employee_id=employee_id).delete()
                for unavailable_day in body['unavailable_days']:
                    employee_unavailable_day = UnavailableDay(weekday=unavailable_day, employee=employee)
                    session.add(employee_unavailable_day)

            session.commit()
            response['status'] = True

        except Exception as e:
            session.rollback()
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Employee's profile could not be updated."
            return response

        finally:
            session.close()

        return response

    @view_config(request_method='DELETE')
    def delete_employee(self):

        response = {
            'status': False,
            'error': None
        }

        if 'employee_id' in self.request.GET:
            employee_id = self.request.GET.get('employee_id')
        else:
            response['status'] = False
            response['error'] = "The 'employee_id's value is missing."
            return response

        try:

            session = Session()
            employee = session.query(Employee).filter_by(id=employee_id).first()

            if employee is None:
                response['status'] = False
                response['error'] = "Employee's profile does not exist."
                return response

            session.delete(employee)
            session.commit()

        except Exception as e:
            session.rollback()
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Employee information could not be deleted."
            return response

        finally:
            session.close()

        response['status'] = True

        return response