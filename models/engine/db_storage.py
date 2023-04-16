#!/usr/bin/python3
"""Defines engine for persistence to sql database"""

from os import getenv
from models.base_model import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import (scoped_session)
from sqlalchemy import (create_engine)
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'Review': Review,
    'State': State,
    'User': User
}


class DBStorage:
    """
    'Factory' for generating the engine
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Creates engine for sql
        """
        u = getenv('HBNB_MYSQL_USER')
        p = getenv('HBNB_MYSQL_PWD')
        h = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(u, p, h, db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries db, in current session, all objects
        """
        objs = {}
        if cls:
            # Return all objects in given Class
            if isinstance(cls, str):
                cls = classes[cls]

            for obj in self.__session.query(cls).all():
                key = obj.__class__.__name__ + "." + obj.id
                objs[key] = obj
        else:
            # query all types of objects (User, State, City, Amenity, Place and
            # Review
            for cls in classes.values():
                for obj in self.__session.query(cls).all():
                    key = obj.__class__.__name__ + "." + obj.id
                objs[key] = obj
        return objs

    def new(self, obj):
        """
        Adds the object to the current db session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from current db session
        """
        if obj:
            cls = classes[type(obj).__name__]
            self.__session.query(cls)\
                          .filter(cls.id == obj.id)\
                          .delete()

    def reload(self):
        """
        Creates all tables in the database
        Creates current db session
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Closes the working session"""
        self.__session.close()
 