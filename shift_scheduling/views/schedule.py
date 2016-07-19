import logging
import random


from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_defaults, view_config

from shift_scheduling import Session
from shift_scheduling.views import BaseView
from shift_scheduling.models import Shift, Employee, Role, UnavailableDay


@view_defaults(route_name='schedule', permission=NO_PERMISSION_REQUIRED, renderer="json")
class ScheduleView(BaseView):

    @view_config(request_method='GET')
    def get_schedule(self):

        response = {
            'status': False,
            'error': None
        }

        try:
            session = Session()

            # fetch employees information
            employees = []
            all_employees = list(session.query(Employee).all())
            for an_employee in all_employees:
                roles = session.query(Role).filter_by(employee_id=an_employee.id).all()
                unavailable_days = session.query(UnavailableDay).filter_by(employee_id=an_employee.id).all()

                employee = {
                    "firstname": an_employee.firstname,
                    "lastname": an_employee.lastname,
                    "roles": [],
                    "maxhours": an_employee.maxhours,
                    "unavailable_days": []
                }
                for role in roles:
                    employee['roles'].append(role.rolename)
                for unavailable_day in unavailable_days:
                    employee['unavailable_days'].append(unavailable_day.weekday)
                employees.append(employee)

            # fetch shifts information
            shifts_dict = {}
            for value in session.query(Shift.weekday).distinct():
                shifts_dict[value.weekday] = []

            shifts = list(session.query(Shift).all())
            for shift in shifts:
                role_hour_pair = {
                    "role": shift.rolename,
                    'hours': shift.hours
                }
                shifts_dict[shift.weekday].append(role_hour_pair)

            schedule = self.generate_schedule(employees, shifts_dict)


        except Exception as e:
            session.rollback()
            logging.error(str(e))
            response['status'] = False
            response['error'] = "Employee/Shift information could not be read."
            return response

        finally:
            session.close()

        response['status'] = True
        response['schedule'] = schedule

        return response

    def generate_schedule(self, employees, shifts_dict):
        scheduler = Scheduler(employees=employees, shifts_dict=shifts_dict)
        return scheduler.schedule()

class Scheduler:

    def __init__(self, employees, shifts_dict):
        self.employees = employees
        self.shifts_dict = shifts_dict

        self.population_size = 10
        self.current_population = []
        self.new_population = []
        self.best_solution_dict = {}
        self.max_iteration = 1000

    def schedule(self):
        self.initialise_ga()
        self.perform_ga()

        return self.format_schedule()

    def format_schedule(self):
        solution_dict = {}
        for key in self.best_solution_dict:
            solution_dict[key] = []
            for i in range(0, len(self.best_solution_dict[key])):
                value = self.best_solution_dict[key][i]
                if value != 0:
                    employee = self.employees[i]
                    shift = self.shifts_dict[key][value-1]
                    employee_shift = {}
                    employee_shift['employee'] = employee
                    employee_shift['shift'] = shift
                    solution_dict[key].append(employee_shift)
        return solution_dict

    def fitness(self, solution_dict):
        positive_award = 1
        negative_award = 100
        role_award = 0
        hours_award = 0
        availability_award = 0
        cost = 1

        # 1. calculate role award
        for key in solution_dict.keys():
            for i in range(0, len(self.employees)):
                value = solution_dict[key][i]
                if value != 0:
                    assigned_role = self.shifts_dict[key][value - 1]['role']
                    actual_roles = self.employees[i]['roles']
                    if assigned_role in actual_roles:
                        role_award += positive_award
                    else:
                        role_award += negative_award

        # print("Role award: " + str(role_award))

        # 2. calculate hours award
        for i in range(0, len(self.employees)):
            assigned_hours = 0
            for key in solution_dict.keys():
                value = solution_dict[key][i]
                if value != 0:
                    assigned_hours += self.shifts_dict[key][value - 1]['hours']
            max_hours = self.employees[i]['maxhours']
            if assigned_hours <= max_hours:
                hours_award += positive_award
            else:
                hours_award += negative_award

        # print("Hours award: " + str(hours_award))

        # 3. calculate availability award
        for key in solution_dict.keys():
            for i in range(0, len(self.employees)):
                value = solution_dict[key][i]
                if value != 0:
                    if key in self.employees[i]['unavailable_days']:
                        availability_award += negative_award
                    else:
                        availability_award += positive_award

        # print("Availability award: " + str(availability_award))

        # 4. calculate cost # NOT SUPPORTED YET
        '''
        for key in solution_dict.keys():
            for i in range(0, len(self.employees)):
                value = solution_dict[key][i]
                if value != 0:
                    assigned_hours = self.shifts_dict[key][value - 1]['hours']
                    cost += assigned_hours * self.employees[i]['salary']

        # print("Cost: " + str(cost))
        '''


        fitness = - role_award * hours_award * availability_award * cost

        return fitness

    def generate_solution_dict(self):
        solution_dict = {}
        for key in self.shifts_dict:
            solution_dict[key] = [0 for x in self.employees]
            for i in range(0, len(self.shifts_dict[key])):
                solution_dict[key][i] = i + 1
            random.shuffle(solution_dict[key])

        return solution_dict

    def initialise_ga(self):

        for i in range(0, self.population_size):
            solution_dict = self.generate_solution_dict()
            self.current_population.append(solution_dict)

        self.best_solution_dict = self.current_population[0]

    def perform_mutation(self, solution_dict):

        cur_fitness = self.fitness(solution_dict)

        muted_solution_dict = {}
        for key in solution_dict:
            muted_solution_dict[key] = list(solution_dict[key])

        # randomly select a day
        keys = list(muted_solution_dict.keys())
        index = random.randint(0, len(keys) - 1)
        day = keys[index]

        solution_day = muted_solution_dict[day]

        # perform swapping
        i = random.randint(0, len(solution_day) - 1)
        j = random.randint(0, len(solution_day) - 1)

        solution_day[i], solution_day[j] = solution_day[j], solution_day[i]

        muted_fitness = self.fitness(muted_solution_dict)

        if cur_fitness >= muted_fitness:
            return solution_dict
        return muted_solution_dict

    def perform_ga(self):
        itr = 0
        while itr < self.max_iteration:
            itr += 1

            self.new_population = []
            for solution_dict in self.current_population:
                muted_solution_dict = self.perform_mutation(solution_dict)
                self.new_population.append(muted_solution_dict)

            sorted(self.new_population, key=self.fitness)

            cur_best_fitness = self.fitness(self.best_solution_dict)
            best_from_new_population = self.new_population[self.population_size - 1]
            muted_best_fitness = self.fitness(best_from_new_population)

            if muted_best_fitness > cur_best_fitness:
                self.best_solution_dict = {}
                for key in best_from_new_population:
                    self.best_solution_dict[key] = list(best_from_new_population[key])

            self.current_population = []
            for population in self.new_population:
                self.current_population.append(population)

            #latest_fitness = self.fitness(self.best_solution_dict)
            #print("Fitness: " + str(latest_fitness))