import json

from shift_scheduling.tests.integration import IntegrationTestBase


class ShiftIntegrationTestViews(IntegrationTestBase):


    def test_crud_on_shift(self):
        """
        It performs CRUD operations on a shift.
        :return:
        """

        # 0. Cleaning up the shifts on 'SUN'
        weekday = 'SUN'
        self.app.delete('/shift?weekday=' + str(weekday))

        # 1. Creating a shift's entry
        data = {
            "weekday": weekday,
            "role_hour_pairs": [
                {
                    "role": "Manager",
                    "hours": 9
                },
                {
                    "role": "Chef",
                    "hours": 8
                },
                {
                    "role": "Chef",
                    "hours": 6
                },
                {
                    "role": "Cook",
                    "hours": 8
                },
                {
                    "role": "Cook",
                    "hours": 4
                },
                {
                    "role": "Dishwasher",
                    "hours": 5
                },
                {
                    "role": "Dishwasher",
                    "hours": 5
                }
            ]
        }
        post_response = self.app.post('/shift', params=json.dumps(data).encode('utf-8'))
        post_result = json.loads(post_response.body.decode('utf-8'))
        self.assertEqual(post_result['status'], True)
        self.assertIsNone(post_result['error'])


        # 2. Reading the shift's entry
        get_response = self.app.get('/shift?weekday=' + str(weekday))
        get_result = json.loads(get_response.body.decode('utf-8'))
        self.assertEqual(get_result['status'], True)
        self.assertIsNone(get_result['error'])
        self.assertEqual(get_result['role_hour_pairs'], data['role_hour_pairs'])


        # 3. Updating the shift's information

        new_data = {
            "weekday": weekday,
            "role_hour_pairs": [
                {
                    "role": "Manager",
                    "hours": 4
                },
                {
                    "role": "Chef",
                    "hours": 5
                },
                {
                    "role": "Chef",
                    "hours": 4
                },
                {
                    "role": "Cook",
                    "hours": 8
                },
                {
                    "role": "Cook",
                    "hours": 7
                },
                {
                    "role": "Dishwasher",
                    "hours": 7
                }
            ]
        }
        update_response = self.app.put('/shift', params=json.dumps(new_data).encode('utf-8'))

        update_result = json.loads(update_response.body.decode('utf-8'))
        self.assertEqual(update_result['status'], True)
        self.assertIsNone(update_result['error'])


        # 4. Reading the updated shift information
        get_response = self.app.get('/shift?weekday=' + str(weekday))
        get_result = json.loads(get_response.body.decode('utf-8'))
        self.assertEqual(get_result['status'], True)
        self.assertIsNone(get_result['error'])
        self.assertEqual(get_result['role_hour_pairs'], new_data['role_hour_pairs'])

        # 5. Deleting the shift's information
        delete_response = self.app.delete('/shift?weekday=' + str(weekday))
        delete_result = json.loads(delete_response.body.decode('utf-8'))
        self.assertEqual(delete_result['status'], True)
        self.assertIsNone(delete_result['error'])

        # 6. Reading the deleted shift
        get_response = self.app.get('/shift?weekday=' + str(weekday))
        get_result = json.loads(get_response.body.decode('utf-8'))
        self.assertEqual(get_result['status'], False)
        self.assertIsNotNone(get_result['error'])
