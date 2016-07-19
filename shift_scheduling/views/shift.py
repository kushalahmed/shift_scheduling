import json
import logging

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_defaults, view_config

from shift_scheduling import Session
from shift_scheduling.views import BaseView
from shift_scheduling.models import Shift


@view_defaults(route_name='shift', permission=NO_PERMISSION_REQUIRED, renderer="json")
class ShiftView(BaseView):

    @view_config(request_method='POST')
    def post_shift(self):

        response = {
            'status': False,
            'error': None
        }

        body = json.loads(self.request.body.decode('utf-8'))

        if 'weekday' in body:
            weekday = body['weekday']
        else:
            response['status'] = False
            response['error'] = "The 'weekday's value is missing."
            return response

        role_hour_pairs = []
        if 'role_hour_pairs' in body:
            role_hour_pairs = body['role_hour_pairs']

        try:
            session = Session()
            # Add shift entry
            for role_hour_pair in role_hour_pairs:
                shift = Shift(rolename=role_hour_pair['role'], weekday=weekday, hours=role_hour_pair['hours'])
                session.add(shift)

            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Shift(s) could not be created."
            return response

        finally:
            session.close()

        response['status'] = True

        return response

    @view_config(request_method='GET')
    def get_shift(self):

        response = {
            'status': False,
            'error': None
        }

        if 'weekday' in self.request.GET:
            weekday = self.request.GET.get('weekday')
        else:
            response['status'] = False
            response['error'] = "The 'weekday's value is missing."
            return response

        try:
            session = Session()
            shifts = session.query(Shift).filter_by(weekday=weekday).all()

        except Exception as e:
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Shift(s) information could not be read."
            return response

        if len(shifts) == 0:
            response['status'] = False
            response['error'] = "Shift(s) information does not exist."
            return response

        response = {
            "status": True,
            "error": None,
            "weekday": weekday,
            "role_hour_pairs": [],
        }

        for shift in shifts:
            role_hour_pair = {
                "role": shift.rolename,
                "hours": shift.hours
            }
            response['role_hour_pairs'].append(role_hour_pair)

        return response

    @view_config(request_method=["PUT", "UPDATE"])
    def update_shift(self):

        response = {
            'status': False,
            'error': None
        }

        body = json.loads(self.request.body.decode('utf-8'))

        if 'weekday' in body:
            weekday = body['weekday']
        else:
            response['status'] = False
            response['error'] = "The 'weekday's value is missing."
            return response

        role_hour_pairs = []
        if 'role_hour_pairs' in body:
            role_hour_pairs = body['role_hour_pairs']

        try:
            session = Session()

            # Delete existing ones
            session.query(Shift).filter_by(weekday=weekday).delete()

            # Add shift entry
            for role_hour_pair in role_hour_pairs:
                shift = Shift(rolename=role_hour_pair['role'], weekday=weekday, hours=role_hour_pair['hours'])
                session.add(shift)

            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Shift(s) could not be updated."
            return response

        finally:
            session.close()

        response['status'] = True

        return response

    @view_config(request_method='DELETE')
    def delete_shift(self):

        response = {
            'status': False,
            'error': None
        }

        if 'weekday' in self.request.GET:
            weekday = self.request.GET.get('weekday')
        else:
            response['status'] = False
            response['error'] = "The 'weekday's value is missing."
            return response

        try:
            session = Session()

            shifts = session.query(Shift).filter_by(weekday=weekday).all()

            if len(shifts) == 0:
                response['status'] = False
                response['error'] = "Shifts information do not exist."
                return response

            for shift in shifts:
                session.delete(shift)

            #session.query(Shift).filter_by(weekday=weekday).delete()
            session.commit()

        except Exception as e:
            session.rollback()
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Shift(s) information could not be deleted."
            return response

        finally:
            session.close()

        response['status'] = True

        return response