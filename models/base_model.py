#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.orm import (declarative_base)
from sqlalchemy import Column, String, DateTime
from models import storage

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60),
                unique=True,
                nullable=False,
                primary_key=True)
    created_at = Column(DateTime,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime,
                        nullable=True,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    v = datetime.strptime(v,
                                        '%Y-%m-%dT%H:%M:%S.%f')
                if k != '___class__':
                    setattr(self, k, v)
                if 'id' not in kwargs.keys():
                    setattr(self, 'id', str(uuid.uuid4))
                time = datetime.now()
                if 'created_at' not in kwargs.keys():
                    setattr(self, 'created_at', time)
                if "updated_at" not in kwargs.keys():
                    setattr(self, 'updated_at', time)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = dict(self.__dict__)
        dictionary['__class__'] = str(type(self).__name__)
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Deletes current instance from storage"""
        storage.delete(self)
