

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Sequence, Unicode, Enum
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import ForeignKey

Base = declarative_base()
Session = sessionmaker()

Rolenames = ('Manager', 'Chef', 'Cook', 'Dishwasher')
Weekdays = ('SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI')

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, Sequence(__tablename__ + '_sq'), primary_key=True)
    firstname = Column(Unicode(100), nullable=False)
    lastname = Column(Unicode(100), nullable=False)
    maxhours = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Employee ('{0}')>".format(self.firstname + ' ' + self.lastname)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id', ondelete="cascade"))
    rolename = Column(Enum(*Rolenames), nullable=False)

    employee = relationship("Employee", back_populates="roles", cascade="all")

    def __repr__(self):
        return "<Role (rolename='%s')>" % self.rolename

Employee.roles = relationship("Role", order_by=Role.id, back_populates="employee", cascade="all")


class UnavailableDay(Base):
    __tablename__ = 'unavailable_days'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id', ondelete="cascade"))
    weekday = Column(Enum(*Weekdays), nullable=False)

    employee = relationship("Employee", back_populates="unavailable_days", cascade="all")

    def __repr__(self):
        return "<Unavailable Day (name='%s')>" % self.weekday

Employee.unavailable_days = relationship("UnavailableDay", order_by=UnavailableDay.id, back_populates="employee", cascade="all")

class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    rolename = Column(Enum(*Rolenames), nullable=False)
    weekday = Column(Enum(*Weekdays), nullable=False)
    hours = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Shift (ID='%s')>" % self.id