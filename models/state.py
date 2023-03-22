#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage
from models.city import City
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    class State(BaseModel, Base):
        """ States model for Database"""
        __tablename__ = "states"
        name = Column(String(128),
                      nullable=False)
        cities = relationship("City",
                              backref='state',
                              cascade='all, delete, delete-orphan')
else:
    class State(BaseModel):
        """Plain model clas for the file storage"""
        name = ""

        def __set_cities(self):
            """
            populates cities property with cities in the state
            """
            cities = storage.all(City).values()
            self.__cities = [city
                             for city in cities
                             if self.id == city.state_id]

        def __get_cities(self):
            """
            gets a list of states with the given state_id
            """
            return self.__cities
        cities = property(__get_cities, __set_cities)
