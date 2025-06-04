from pydantic import BaseModel, EmailStr
from typing import Optional

class GeoBase(BaseModel):
    lat: str
    lng: str

class GeoCreate(GeoBase):
    pass

class Geo(GeoBase):
    id: int
    address_id: int

    class Config:
        from_attributes = True

class AddressBase(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str

class AddressCreate(AddressBase):
    geo: GeoCreate

class Address(AddressBase):
    id: int
    user_id: int
    geo: Geo

    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str
    catchPhrase: str
    bs: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str
    website: str

class UserCreate(UserBase):
    password: str
    address: AddressCreate
    company: CompanyCreate

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    address: Address
    company: Company

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 