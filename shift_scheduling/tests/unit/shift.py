import json

from pyramid import testing

from shift_scheduling.tests.unit import UnitTestsViews
from shift_scheduling.views.employee import EmployeeView
from shift_scheduling.views.shift import ShiftView


class ShiftViewUnitTests(UnitTestsViews):

    def test_create_shift_null_weekday_value(self):
        request = testing.DummyRequest()
        data = {
            #"weekday": "SUN",
            "role_hour_pairs": [
                {
                    "role": "Manager",
                    "hours": 8
                },
                {
                    "role": "Cook",
                    "hours": 5
                }
            ]
        }
        request.body = json.dumps(data).encode('utf-8')
        shift = ShiftView(request)
        response = shift.post_shift()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_create_shift_invalid_role_value(self):
        request = testing.DummyRequest()
        data = {
            "weekday": "SUN",
            "role_hour_pairs": [
                {
                    "role": "X_Manager",
                    "hours": 8
                },
                {
                    "role": "Cook",
                    "hours": 5
                }
            ]
        }
        request.body = json.dumps(data).encode('utf-8')
        shift = ShiftView(request)
        response = shift.post_shift()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_create_shift_with_valid_values(self):

        data = {
            "weekday": "SUN",
            "role_hour_pairs": [
                {
                    "role": "Manager",
                    "hours": 8
                },
                {
                    "role": "Cook",
                    "hours": 5
                }
            ]
        }

        # clean-up
        request = testing.DummyRequest(params={"weekday": data['weekday']})
        shift = ShiftView(request)
        shift.delete_shift()

        # test code
        request = testing.DummyRequest()
        request.body = json.dumps(data).encode('utf-8')
        shift = ShiftView(request)
        response = shift.post_shift()
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

    def test_read_shift_invalid_weekday(self):
        request = testing.DummyRequest(params={ "weekday" : "X" })
        shift = ShiftView(request)
        response = shift.get_shift()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_read_shift_valid_weekday(self):

        data = {
            "weekday": "SUN",
            "role_hour_pairs": [
                {
                    "role": "Manager",
                    "hours": 8
                },
                {
                    "role": "Cook",
                    "hours": 5
                }
            ]
        }

        # clean-up
        request = testing.DummyRequest(params={"weekday": data['weekday']})
        shift = ShiftView(request)
        shift.delete_shift()

        # test code
        request = testing.DummyRequest()
        request.body = json.dumps(data).encode('utf-8')
        shift = ShiftView(request)
        response = shift.post_shift()
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

        request = testing.DummyRequest(params={"weekday": data['weekday']})
        shift = ShiftView(request)
        response = shift.get_shift()
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])
        self.assertEqual(response['weekday'], data["weekday"])
        self.assertEqual(response['role_hour_pairs'], data["role_hour_pairs"])


    def test_update_update_invalid_weekday(self):

        data = {
            #"weekday": "SUN",
            "role_hour_pairs": [
                {
                    "role": "Manager",
                    "hours": 8
                },
                {
                    "role": "Cook",
                    "hours": 5
                }
            ]
        }

        # clean-up
        request = testing.DummyRequest(params={"weekday": "SUN"})
        shift = ShiftView(request)
        shift.delete_shift()

        # test code
        request = testing.DummyRequest()
        request.body = json.dumps(data).encode('utf-8')

        shift = ShiftView(request)
        response = shift.update_shift()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_update_shift_valid_weekday(self):

        old_data = {
            "weekday": "SUN",
            "role_hour_pairs": [
                {
                    "role": "Cook",
                    "hours": 6
                },
                {
                    "role": "Chef",
                    "hours": 8
                }
            ]
        }

        # clean-up
        request = testing.DummyRequest(params={"weekday": old_data['weekday']})
        shift = ShiftView(request)
        shift.delete_shift()

        # test code
        request = testing.DummyRequest()
        request.body = json.dumps(old_data).encode('utf-8')
        shift = ShiftView(request)
        response = shift.post_shift()

        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])


        new_data = {
            "weekday": "SUN",
            "role_hour_pairs": [
                {
                    "role": "Manager",
                    "hours": 8
                },
                {
                    "role": "Dishwasher",
                    "hours": 8
                }
            ]
        }

        request.body = json.dumps(new_data).encode('utf-8')

        shift = ShiftView(request)
        response = shift.update_shift()
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

        request = testing.DummyRequest(params={"weekday": new_data['weekday']})
        shift = ShiftView(request)
        response = shift.get_shift()
        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])
        self.assertEqual(response['weekday'], new_data["weekday"])
        self.assertEqual(response['role_hour_pairs'], new_data["role_hour_pairs"])


    def test_delete_shift_invalid_weekday(self):
        request = testing.DummyRequest(params={"weekday": "X"})
        shift = ShiftView(request)
        response = shift.delete_shift()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])

    def test_delete_shift_valid_weekday(self):

        data = {
            "weekday": "SUN",
            "role_hour_pairs": [
                {
                    "role": "Cook",
                    "hours": 6
                },
                {
                    "role": "Chef",
                    "hours": 8
                }
            ]
        }

        # clean-up
        request = testing.DummyRequest(params={"weekday": data['weekday']})
        shift = ShiftView(request)
        shift.delete_shift()

        # test code
        request = testing.DummyRequest()
        request.body = json.dumps(data).encode('utf-8')
        shift = ShiftView(request)
        response = shift.post_shift()

        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

        request = testing.DummyRequest(params={"weekday": data['weekday']})
        shift = ShiftView(request)
        response = shift.delete_shift()

        self.assertEqual(response['status'], True)
        self.assertIsNone(response['error'])

        # Reading again, should return 'False' status
        request = testing.DummyRequest(params={"weekday": data['weekday']})
        shift = ShiftView(request)
        response = shift.get_shift()
        self.assertEqual(response['status'], False)
        self.assertIsNotNone(response['error'])