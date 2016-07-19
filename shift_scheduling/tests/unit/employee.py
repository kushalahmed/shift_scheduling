import json

from pyramid import testing

from shift_scheduling.tests.unit import UnitTestsViews
from shift_scheduling.views.employee import EmployeeView


class EmployeeViewUnitTests(UnitTestsViews):

    def test_create_employee_null_firstname_value(self):
        request = testing.DummyRequest()
        data = {
            #"firstname": "Kushal",
            "lastname": "Ahmed",
            "roles": ["Manager", "Chef"],
            "maxhours": 40,
            "unavailable_days": ["SAT", "SUN"]
        }
        request.body = json.dumps(data).encode('utf-8')
        employee = EmployeeView(request)
        response = employee.post_employee()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_create_employee_null_lastname_value(self):
        request = testing.DummyRequest()
        data = {
            "firstname": "Kushal",
            #"lastname": "Ahmed",
            "roles": ["Manager", "Chef"],
            "maxhours": 40,
            "unavailable_days": ["SAT", "SUN"]
        }
        request.body = json.dumps(data).encode('utf-8')
        employee = EmployeeView(request)
        response = employee.post_employee()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_create_employee_invalid_role_value(self):
        request = testing.DummyRequest()
        data = {
            "firstname": "Kushal",
            "lastname": "Ahmed",
            "roles": ["X_Manager", "Chef"],
            "maxhours": 40,
            "unavailable_days": ["SAT", "SUN"]
        }
        request.body = json.dumps(data).encode('utf-8')
        employee = EmployeeView(request)
        response = employee.post_employee()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_create_employee_invalid_unavailable_day_value(self):
        request = testing.DummyRequest()
        data = {
            "firstname": "Kushal",
            "lastname": "Ahmed",
            "roles": ["Manager", "Chef"],
            "maxhours": 40,
            "unavailable_days": ["X_SAT", "SUN"]
        }
        request.body = json.dumps(data).encode('utf-8')
        employee = EmployeeView(request)
        response = employee.post_employee()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_create_employee_with_valid_values(self):
        request = testing.DummyRequest()
        data = {
            "firstname": "Kushal",
            "lastname": "Ahmed",
            "roles": ["Manager", "Chef", "Cook"],
            "maxhours": 40,
            "unavailable_days": ["SAT", "SUN", "FRI"]
        }
        request.body = json.dumps(data).encode('utf-8')
        employee = EmployeeView(request)
        response = employee.post_employee()
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

    def test_read_employee_invalid_employee_id(self):
        request = testing.DummyRequest(params={ "employee_id" : "X" })
        employee = EmployeeView(request)
        response = employee.get_employee()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_read_employee_valid_employee_id(self):
        request = testing.DummyRequest()
        data = {
            "firstname": "Kushal",
            "lastname": "Ahmed",
            "roles": ["Manager", "Chef", "Cook"],
            "maxhours": 40,
            "unavailable_days": ["SAT", "SUN", "FRI", "THU"]
        }
        request.body = json.dumps(data).encode('utf-8')
        employee = EmployeeView(request)
        response = employee.post_employee()

        self.assertIsNotNone(response['employee_id'])
        employee_id = response['employee_id']

        request = testing.DummyRequest(params={"employee_id": employee_id})
        employee = EmployeeView(request)
        response = employee.get_employee()
        self.assertEqual(response['firstname'], data["firstname"])
        self.assertEqual(response['unavailable_days'], data["unavailable_days"])
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

    def test_update_employee_invalid_employee_id(self):
        request = testing.DummyRequest()
        data = {
            "firstname": "Kushal",
            "lastname": "Ahmed",
            "roles": ["Manager", "Cook"],
            "maxhours": 40,
            "unavailable_days": ["SAT", "THU"]
        }
        request.body = json.dumps(data).encode('utf-8')

        employee = EmployeeView(request)
        response = employee.update_employee()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_update_employee_valid_employee_id(self):
        request = testing.DummyRequest()
        old_data = {
            "firstname": "Kushal",
            "lastname": "Ahmed",
            "roles": ["Chef", "Cook"],
            "maxhours": 30,
            "unavailable_days": ["FRI", "THU"]
        }
        request.body = json.dumps(old_data).encode('utf-8')
        employee = EmployeeView(request)
        response = employee.post_employee()

        self.assertIsNotNone(response['employee_id'])
        employee_id = response['employee_id']

        new_data = {
            "employee_id": employee_id,
            "firstname": "Roha",
            "lastname": "Ahmed",
            "roles": ["Manager"],
            "maxhours": 40,
            "unavailable_days": ["THU"]
        }

        request.body = json.dumps(new_data).encode('utf-8')

        employee = EmployeeView(request)
        response = employee.update_employee()
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

        request = testing.DummyRequest(params={"employee_id": employee_id})
        employee = EmployeeView(request)
        response = employee.get_employee()
        self.assertEqual(response['firstname'], new_data["firstname"])
        self.assertEqual(response['unavailable_days'], new_data["unavailable_days"])
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

    def test_delete_employee_invalid_employee_id(self):
        request = testing.DummyRequest(params={"employee_id": "X"})
        employee = EmployeeView(request)
        response = employee.delete_employee()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_delete_employee_valid_employee_id(self):
        request = testing.DummyRequest()
        data = {
            "firstname": "Kushal",
            "lastname": "Ahmed",
            "roles": ["Chef", "Cook"],
            "maxhours": 30,
            "unavailable_days": ["FRI", "THU"]
        }
        request.body = json.dumps(data).encode('utf-8')
        employee = EmployeeView(request)
        response = employee.post_employee()

        self.assertIsNotNone(response['employee_id'])
        employee_id = response['employee_id']

        request = testing.DummyRequest(params={"employee_id": employee_id})
        employee = EmployeeView(request)
        response = employee.delete_employee()
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

        # Reading again, should return 'False' status
        request = testing.DummyRequest(params={"employee_id": employee_id})
        employee = EmployeeView(request)
        response = employee.get_employee()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])