from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Geo(Base):
    __tablename__ = "geo"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(String)
    lng = Column(String)
    address_id = Column(Integer, ForeignKey("address.id"))

    address = relationship("Address", back_populates="geo")

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    suite = Column(String)
    city = Column(String)
    zipcode = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    geo = relationship("Geo", back_populates="address", uselist=False, cascade="all, delete-orphan")
    user = relationship("User", back_populates="address")

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    catchPhrase = Column(String)
    bs = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="company")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    phone = Column(String)
    website = Column(String)

    address = relationship("Address", back_populates="user", uselist=False, cascade="all, delete-orphan")
    company = relationship("Company", back_populates="user", uselist=False, cascade="all, delete-orphan") 