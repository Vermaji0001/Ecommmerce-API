

from sqlalchemy import Column,Integer,String,TIMESTAMP
from utils.get_db import base




class Coustomer (base):
    __tablename__="coustomerregister"
    id=Column(Integer,primary_key=True)
    coustomer_name=Column(String(20),nullable=False)
    email=Column(String(20),nullable=False,unique=True)
    password=Column(String(200),nullable=False)
    state=Column(String(20),nullable=False)
    address=Column(String(200),nullable=False)
    pincode=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP,nullable=True)



class Manufacturer(base):
    __tablename__="manufacturersignup"
    id=Column(Integer,primary_key=True)
    store_name=Column(String(200),nullable=False)
    manufacturer_name=Column(String(20),nullable=False)
    email=Column(String(200),nullable=False)
    password=Column(String(200),nullable=False)
    created_at=Column(TIMESTAMP,nullable=True)


class Category(base):
    __tablename__="category"
    id=Column(Integer,primary_key=True)
    category_name=Column(String(200),nullable=False)   

class Brand(base):
    __tablename__="brand"
    id=Column(Integer,primary_key=True)
    brand_name=Column(String(200),nullable=False)


class Product(base):
    __tablename__="Product"
    id=Column(Integer,primary_key=True)
    manufacturer_id=Column(Integer,nullable=False)
    product_name=Column(String(200),nullable=False)
    product_type=Column(String(200),nullable=False)
    category=Column(String(200),nullable=False)
    brand=Column(String(200),nullable=False)
    mrp=Column(Integer,nullable=False)
    discount=Column(Integer,nullable=False)
    sale_price=Column(Integer,nullable=True)
         