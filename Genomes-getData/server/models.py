from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Table
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from server import app

#Initialize postgreSQL genome database
engine = create_engine('postgres://localhost/genome', convert_unicode=True)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(session_factory)
Base = declarative_base()
Base.query = db_session.query_property()


try:
    #connect to database if it exissts
    connection = connect(dbname='genome', user=app.config.get('DATABASE_USERNAME'), host='localhost', password=app.config.get('DATABASE_PASSWORD'))
except:
    #create database if it does not already exist
    connection = connect(user=app.config.get('DATABASE_USERNAME'), host='localhost', password=app.config.get('DATABASE_PASSWORD'))
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE genome")
    cursor.close()
    #connection.close()


# Join table between users and relatives, see User model relatives property
user_relatives = Table('user_relatives',
    Base.metadata,
    Column('user_profile_id', String(255), ForeignKey('users.profile_id')),
    Column('relative_id', Integer, ForeignKey('relatives.id'))
    )
#User model Schema
class User(Base):
    __tablename__ = 'users'
    profile_id = Column(String(255), primary_key=True, unique=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    location = Column(String(255), nullable=True)
    picture_url_small = Column(String(255), nullable=True)
    picture_url_medium = Column(String(255), nullable=True)
    picture_url_large = Column(String(255), nullable=True)
    rs12913832 = Column(String(255), nullable=True)

    # Setting up the relationship to the relatives table and user_relatives join table
    relatives = relationship('Relative', secondary=user_relatives, backref=backref('user', lazy='dynamic'))

    def __init__(self, profile_id, email, first_name, last_name, location, picture_url_small, picture_url_medium, picture_url_large, rs12913832):
        self.profile_id = profile_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.location = location
        self.picture_url_small = picture_url_small
        self.picture_url_medium = picture_url_medium
        self.picture_url_large = picture_url_large
        self.rs12913832 = rs12913832

    def create_new_user(profile_id, email,  first_name, last_name, location, picture_url_small, picture_url_medium, picture_url_large):
        # Refactor this later to use kwargs
        # Refactor to get or create user
        new_user = User(profile_id, email, first_name, last_name, location, picture_url_small, picture_url_medium, picture_url_large)

#Relative schema
class Relative(Base):
    __tablename__ = 'relatives'
    id = Column(Integer(), primary_key=True)
    email = Column(String(255), unique=True, nullable=True)
    first_name = Column(String(255), default='Anonymous')
    last_name = Column(String(255), default='')
    sex = Column(String(255))
    residence = Column(String(255), nullable=True)
    similarity = Column(Float())
    maternal_side = Column(Boolean())
    paternal_side = Column(Boolean())
    picture_url = Column(String(255), nullable=True)

    # add userId to init
    def __init__(self, email, first_name, last_name, sex, residence, similarity, maternal_side, paternal_side, picture_url):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.residence = residence
        self.similarity = similarity
        self.maternal_side = maternal_side
        self.paternal_side = paternal_side
        self.picture_url = picture_url

#Snp data schema
class Snp(Base):
    __tablename__ = 'snps'
    id = Column(Integer(), primary_key=True)
    rs_id = Column(String(255))
    dnaPair = Column(String(255))
    outcome = Column(String(255))

    def __init__(self, rs_id, dnaPair, outcome):
        self.rs_id = rs_id
        self.dnaPair = dnaPair
        self.outcome = outcome


Base.metadata.create_all(engine)
