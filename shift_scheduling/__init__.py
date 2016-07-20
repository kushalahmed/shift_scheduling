import logging
import os

import sqlalchemy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy_utils import database_exists, create_database

import data
from .models import Base, Session, Employee, Role, UnavailableDay, Shift


def setup_environment_variables():
    os.environ['MYSQL_ROOT_USER'] = 'root'
    os.environ['MYSQL_ROOT_PASSWORD'] = 'admin'
    os.environ['DB_HOST'] = '127.0.0.1'
    os.environ['DB_PORT'] = '3306'
    os.environ['MYSQL_DB_SCHEMA_NAME'] = 'shiftdb'
    os.environ['INITIALISE_DATABASE_TABLES'] = 'false'
    os.environ['RABBITMQ_HOST'] = '127.0.0.1'
    os.environ['RABBITMQ_PORT'] = '5672'


def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    return dict((key, os.path.expandvars(value)) for
                key, value in settings.items())

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # Setup environment variables
    # Note: activate it if running in the local machine (not in Docker or so)
    #setup_environment_variables()

    # Expand the environment variables in the settings
    settings = expandvars_dict(settings)

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    engine = engine_from_config(settings, 'sqlalchemy.')
    if create_database_schema_if_not_exists(settings.get('sqlalchemy.url')):
        Base.metadata.create_all(engine)

    Session.configure(bind=engine)

    if settings.get('initialise.database.tables') == 'true':
        initialise_database_tables()

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route(name='employee', pattern='/employee')
    config.add_route(name='shift', pattern='/shift')
    config.add_route(name='schedule', pattern='/schedule')

    config.scan()
    return config.make_wsgi_app()


# Returns True if created, False otherwise
def create_database_schema_if_not_exists(schema_url):
    engine = sqlalchemy.create_engine(schema_url)
    if not database_exists(engine.url):
        create_database(engine.url)
        return True
    return False


def initialise_database_tables():
    insert_sample_employees_and_shifts() # A sample initialisation!

def insert_sample_employees_and_shifts():

    try:

        session = Session()

        employees_dict = data.employees
        for employee_dict in employees_dict:
            employee = Employee(firstname=employee_dict['firstname'], lastname=employee_dict['lastname'],
                                maxhours=employee_dict['maxhours'])
            session.add(employee)

            # Add employee role entry
            for rolename in employee_dict['roles']:
                employee_role = Role(rolename=rolename, employee=employee)
                session.add(employee_role)

            # Add unavailable day entry
            for unavailable_day in employee_dict['unavailable_days']:
                employee_unavailable_day = UnavailableDay(weekday=unavailable_day, employee=employee)
                session.add(employee_unavailable_day)
            session.commit()

        shifts_dict = data.shifts
        for shift_dict in shifts_dict:
            weekday = shift_dict['weekday']
            for role_hours_pair in shift_dict['role_hour_pairs']:
                shift = Shift(rolename=role_hours_pair['role'], weekday=weekday, hours=role_hours_pair['hours'])
                session.add(shift)
            session.commit()

    except Exception as e:
        session.rollback()
        logging.error(str(e))
        return False

    finally:
        session.close()

    return True
