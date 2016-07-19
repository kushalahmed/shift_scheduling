How to compile and run:
=======================

    1. Install an instance of Python 3.5.1
    2. Install all the modules enlisted in requirements.txt
    3. Go to the project root folder, and create a distribution by executing the following:
        python setup.py develop
    4. Run the web service by executing the following:
        pserve --reload development.ini


Containerized Web Service (Optional):
=====================================

    Dockerfile, and other necessary scripts have been added to build a Docker image.


How to use the Web Service:
===========================

    1. CRUD operations on Employee:

        1.1 POST

            Sample:
            curl -X POST http://localhost:6542/employee
                {
                    "firstname": "Kushal",
                    "lastname": "Ahmed",
                    "roles": ["Manager", "Chef"],
                    "maxhours": 40,
                    "unavailable_days": ["SAT", "SUN"]
                }

            Response:
            If successful,
                {
                    "status": true,
                    "error": null,
                    "employee_id": 1
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }

            Restrictions:
            1. The fields 'firstname', 'lastname' and 'maxhours' must NOT be null.
            2. The field 'roles' must be a subset of ['Manager', 'Chef', 'Cook', 'Dishwasher']
            3. The field 'unavailable_days' must be a subset of ['SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI']

        1.2 GET

            Sample:
            curl GET http://localhost:6542/employee?employee_id=1

            Response:
            If successful,
                {
                   "status": true,
                   "error": null,
                   "firstname": "Kushal",
                   "lastname": "Ahmed",
                   "roles": ["Manager", "Chef"],
                   "maxhours": 40,
                   "unavailable_days": ["SAT", "SUN"]
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }

        1.3 UPDATE/PUT

            Sample:
            curl PUT http://localhost:6542/employee
                {
                    "employee_id": 1,
                    "firstname": "Mehbub",
                    "lastname": "Rahman",
                    "roles": ["Manager", "Cook"],
                    "maxhours": 30,
                    "unavailable_days": ["SAT", "MON"]
                }

            Response:
            If successful,
                {
                    "status": true,
                    "error": null
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }

        1.4 DELETE

            Sample:
            curl DELETE http://localhost:6542/employee?employee_id=1

            Response:
            If successful,
                {
                    "status": true,
                    "error": null
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }


    2. CRUD operations on Shift:

        2.1 POST

            Sample:
            curl -X POST http://localhost:6542/shift
                {
                    "weekday": "SUN",
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

            Response:
            If successful,
                {
                    "status": true,
                    "error": null
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }

        2.2 GET

            Sample:
            curl GET http://localhost:6542/shift?weekday=SAT

            Response:
            If successful,
                {
                    "status": true,
                    "error": null,
                    "weekday": "SAT",
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
                            "hours": 4
                        },
                        {
                            "role": "Cook",
                            "hours": 7
                        },
                        {
                            "role": "Cook",
                            "hours": 3
                        },
                        {
                            "role": "Dishwasher",
                            "hours": 8
                        }
                    ]
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }


        2.3 UPDATE/PUT

            Sample:
            curl PUT http://localhost:6542/shift
                {
                    "weekday": "SUN",
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

            Response:
            If successful,
                {
                    "status": true,
                    "error": null
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }

        2.4 DELETE

            Sample:
            curl DELETE http://localhost:6542/shift?weekday=SAT

            Response:
            If successful,
                {
                    "status": true,
                    "error": null
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }

    3. Schedule shifts for the employees:

        3.1 GET

            It assumes that the database tables holds the employee and shifts information. It reads the database tables, and generates a schedule.

            The schedule contains shifts and comployees information for each week day.

            Sample:
            curl GET http://localhost:6542/schedule


            Response:
            If successful,
                {
                    "status": true,
                    "error": null,
                    "schedule": {
                        "SAT": [
                            {
                                "shift": {
                                    "hours": 9,
                                    "role": "Manager"
                                },
                                "employee": {
                                    "maxhours": 40,
                                    "lastname": "Dew",
                                    "unavailable_days": [
                                        "Mon"
                                        ],
                                    "roles": [
                                        "Manager",
                                        "Chef"
                                        ],
                                    "firstname": "Steve"
                                }
                            },
                            {
                                "shift": {
                                    "hours": 3,
                                    "role": "Cook"
                                },
                                "employee": {
                                    "maxhours": 30,
                                    "lastname": "Li",
                                    "unavailable_days": [],
                                    "roles": [
                                        "Cook"
                                        ],
                                    "firstname": "Hanxi"
                                }
                            }
                            ],
                        "SUN": [
                            {
                                "shift": {
                                    "hours": 9,
                                    "role": "Manager"
                                },
                                "employee": {
                                    "maxhours": 40,
                                    "lastname": "Dew",
                                    "unavailable_days": [
                                        "Mon"
                                        ],
                                    "roles": [
                                        "Manager",
                                        "Chef"
                                        ],
                                    "firstname": "Steve"
                                }
                            },
                            {
                                "shift": {
                                    "hours": 4,
                                    "role": "Cook"
                            },
                                "employee": {
                                    "maxhours": 30,
                                    "lastname": "Kandjani",
                                    "unavailable_days": [],
                                    "roles": [
                                        "Cook",
                                        "Chef"
                                        ],
                                    "firstname": "Hadi"
                                    }
                            }
                        ]
                    }
                }

            If unsuccessful,
                {
                    "status": false,
                    "error": "<ERROR MESSAGE>"
                }