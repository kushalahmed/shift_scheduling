import json

from shift_scheduling.tests.integration import IntegrationTestBase


class EmployeeIntegrationTestViews(IntegrationTestBase):


    def test_crud_on_employee_profile(self):
        """
        It performs CRUD operations on an employee's profile.
        :return:
        """

        # 1. Creating an employee's profile
        data = {
            "firstname": "Roha",
            "lastname": "Ahmed",
            "roles": ["Manager", "Chef"],
            "maxhours": 30,
            "unavailable_days": ["SAT", "MON"]
        }
        post_response = self.app.post('/employee', params=json.dumps(data).encode('utf-8'))
        post_result = json.loads(post_response.body.decode('utf-8'))
        self.assertIsNotNone(post_result['employee_id'])
        employee_id = post_result['employee_id']

        # 2. Reading the employee's profile
        get_response = self.app.get('/employee?employee_id=' + str(employee_id))
        get_result = json.loads(get_response.body.decode('utf-8'))
        self.assertEqual(get_result['status'], True)
        self.assertIsNone(get_result['error'])
        self.assertEqual(get_result['firstname'], data['firstname'])
        self.assertEqual(get_result['lastname'], data['lastname'])
        self.assertEqual(get_result['maxhours'], data['maxhours'])
        self.assertEqual(get_result['roles'], data['roles'])
        self.assertEqual(get_result['unavailable_days'], data['unavailable_days'])

        # 3. Updating the profile's information

        new_data = {
            "employee_id": employee_id,
            "firstname": "Ahladita",
            "lastname": "Ahmed",
            "roles": ["Cook"],
            "maxhours": 40,
            "unavailable_days": ["SAT", "SUN"]
        }
        update_response = self.app.put('/employee', params=json.dumps(new_data).encode('utf-8'))

        update_result = json.loads(update_response.body.decode('utf-8'))
        self.assertEqual(update_result['status'], True)
        self.assertIsNone(update_result['error'])

        # 4. Reading the updated profile information
        get_response = self.app.get('/employee?employee_id=' + str(employee_id))
        get_result = json.loads(get_response.body.decode('utf-8'))
        self.assertEqual(get_result['status'], True)
        self.assertIsNone(get_result['error'])
        self.assertEqual(get_result['firstname'], new_data['firstname'])
        self.assertEqual(get_result['lastname'], new_data['lastname'])
        self.assertEqual(get_result['maxhours'], new_data['maxhours'])
        self.assertEqual(get_result['roles'], new_data['roles'])
        self.assertEqual(get_result['unavailable_days'], new_data['unavailable_days'])

        # 5. Deleting the employee's profile
        delete_response = self.app.delete('/employee?employee_id=' + str(employee_id))
        delete_result = json.loads(delete_response.body.decode('utf-8'))
        self.assertEqual(delete_result['status'], True)
        self.assertIsNone(delete_result['error'])

        # 6. Reading the deleted profile
        get_response = self.app.get('/employee?employee_id=' + str(employee_id))
        get_result = json.loads(get_response.body.decode('utf-8'))
        self.assertEqual(get_result['status'], False)
        self.assertIsNotNone(get_result['error'])