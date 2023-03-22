#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship


if getenv('HBNB_TYPE_STORAGE') == 'db':
    class Place(BaseModel, Base):
        """Table Schema for place data"""
        __tablename__ = "places"
        city_id = Column(String(60),
                         ForeignKey('cities.id'),
                         nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id'),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer(), nullable=False, default=0)
        number_bathrooms = Column(Integer(), nullable=False, default=0)
        max_guest = Column(Integer(), nullable=False, default=0)
        price_by_night = Column(Integer(), nullable=False, default=0)
        latitude = Column(Float(), nullable=True)
        longitude = Column(Float(), nullable=True)
        amenity_ids = []

        reviews = relationship('Review', backref='place',
                               cascade="all, delete, delete-orphan")
        amenities = relationship('Amenity', secondary='place_amenity',
                                 viewonly=False)

        def __init__(self, *args, **kwargs):
            """Initializes Place"""
            super().__init__(*args, **kwargs)
else:
    class Place(BaseModel):
        """ A place to stay """
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
