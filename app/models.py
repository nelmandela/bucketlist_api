from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date,DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask_bcrypt import Bcrypt
# from app import db

 
engine = create_engine('sqlite:///test_db', echo=True)
Base = declarative_base()
 

class User(Base):

    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)  
    password = Column(String)
    bucketlists = relationship('Bucketlist', back_populates='user')
    
    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def compare_password(self, password):
        return Bcrypt().check_password_hash(self.password, password)
        

class Bucketlist(Base):

    __tablename__ = "bucketlists"

    id = Column(Integer, primary_key=True)
    bucketlist_id = Column(String)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='bucketlists')
    bucketlist_items = relationship('Bucketlist_item', back_populates='bucketlist')

    def __init__(self, bucketlist_id, created_by):
        self.bucketlist_id = bucketlist_id
        self.created_by = created_by

class Bucketlist_item(Base):

    __tablename__ = "bucketlist_items"

    id = Column(Integer, primary_key=True)
    bucketlist_item_id = Column(String)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    bucketlist_id = Column(Integer, ForeignKey('bucketlists.id'))
    created_by = Column(Integer, ForeignKey('users.id'))
    bucketlist = relationship('Bucketlist', back_populates='bucketlist_items')


    def __init__(self, bucketlist_id, bucketlist_item_id):
        self.bucketlist_id = bucketlist_id
        self.bucketlist_item_id = bucketlist_item_id

Base.metadata.create_all(engine)        