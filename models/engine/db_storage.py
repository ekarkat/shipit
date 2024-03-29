#!/usr/bin/bash
"""Database storage class"""
import os
from sys import argv
from models.user import User
from models.city import City
from models.agent import Agent
from models.state import State
from dotenv import load_dotenv
from models.parcel import Parcel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine, func
from models.base_model import BaseModel, Base


class DBStorage():
    # Database storage class
    __engine = None
    __session = None

    def __init__(self):
        """Start engine"""
        load_dotenv()
        # Read the environment variables
        mysql_user = os.getenv("MYSQL_USER")
        mysql_pwd = os.getenv("MYSQL_PWD")
        mysql_host = os.getenv("MYSQL_HOST")
        mysql_db = os.getenv("MYSQL_DB")

        # Construct the connection string
        connection_string = f"mysql+mysqldb://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}?charset=utf8"

        # Create engine
        self.__engine = create_engine(connection_string, pool_pre_ping=True)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objs_dic = {}
        if not cls:
            result = self.__session.query(User).all()
            result.extend(self.__session.query(Parcel).all())
            result.extend(self.__session.query(State).all())
            result.extend(self.__session.query(City).all())
        else:
            if isinstance(cls, str):
                result = self.__session.query(eval(cls)).all()
            else:
                result = self.__session.query(cls).all()
        for obj in result:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objs_dic[key] = obj
        return (objs_dic)

    def user_by_email(self, email):
        """Returns a user based on email"""
        result = self.__session.query(User).filter_by(user_email=email).all()
        if len(result) == 0:
            return None
        return (result[0])

    def user_id(self, id):
        """Returns a user based on id"""
        result = self.__session.query(User).filter_by(id=id).all()
        if len(result) == 0:
            return None
        return (result[0])

    def agent_id(self, id):
        """Returns a user based on id"""
        result = self.__session.query(Agent).filter_by(id=id).all()
        if len(result) == 0:
            return None
        return (result[0])

    def agent_eamil(self, email):
        """Returns a user based on email"""
        result = self.__session.query(Agent).filter_by(agent_email=email).all()
        if len(result) == 0:
            return None
        return (result[0])

    def parcel_id(self, id):
        """Returns a user based on id"""
        result = self.__session.query(Parcel).filter_by(id=id).all()
        if len(result) == 0:
            return None
        return (result[0])

    def parcel_track(self, track_num):
        """Returns a user based on id"""
        result = self.__session.query(Parcel).filter_by(parcel_tracking_number=track_num).all()
        if len(result) == 0:
            return None
        return (result[0])
    
    def count_parcels(self):
        """Returns the total number of parcels"""
        return self.__session.query(func.count(Parcel.id)).scalar()
    
    def count_users(self):
        """Returns the total number of users"""
        return self.__session.query(func.count(User.id)).scalar()

    def new(self, obj):
        """Add obj to database"""
        self.__session.add(obj)

    def save(self):
        """commit changes in database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def ses(self):
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        ses = Session()
        return (ses)

    def close(self):
        # close a session
        self.__session.close()
