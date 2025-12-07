

from sqlalchemy import Column,Integer,String,TIMESTAMP
from sqlalchemy.orm import relationship
from utils.get_db import base
from sqlalchemy import ForeignKey




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
    profile=relationship("CoustomerProfile",back_populates="coustomer",cascade="all,delete-orphan")
    order=relationship("OrderPlaced",back_populates="coustomer",cascade="all,delete-orphan")



class Manufacturer(base):
    __tablename__="manufacturersignup"
    id=Column(Integer,primary_key=True)
    store_name=Column(String(200),nullable=False)
    manufacturer_name=Column(String(20),nullable=False)
    email=Column(String(200),nullable=False)
    password=Column(String(200),nullable=False)
    created_at=Column(TIMESTAMP,nullable=True)
    profile=relationship("ManufacturerProfile",back_populates="manufacturer",cascade="all,delete-orphan")
    product=relationship("Product",back_populates="manufacturer",cascade="all,delete-orphan",uselist=True)


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
    manufacturer_id=Column(Integer,ForeignKey("manufacturersignup.id",ondelete='CASCADE'),nullable=False)
    product_name=Column(String(200),nullable=False)
    product_type=Column(String(200),nullable=False)
    category=Column(String(200),nullable=False)
    product_quantity=Column(Integer,nullable=False)
    brand=Column(String(200),nullable=False)
    mrp=Column(Integer,nullable=False)
    discount_percentage=Column(Integer,nullable=False)
    sale_price=Column(Integer,nullable=True)
    manufacturer=relationship("Manufacturer",back_populates="product",uselist=True)



class Otp(base):
    __tablename__="otp"
    id=Column(Integer,primary_key=True)
    email=Column(String(200),nullable=False)
    otp=Column(Integer,nullable=False)
    

class AddToCart(base):
    __tablename__="addTocart"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,nullable=False)
    product_id=Column(Integer,nullable=False)
    product_quantity=Column(Integer,nullable=False)


# class ProductPayment(base):
#     id=Column(Integer,primary_key=True)
#     coustomer_id=Column(Integer,nullable=False)
#     Product_id=Column(Integer,nullable=False)
#     total_payment=Column(Integer,nullable=True)
#     payment_status=Column(String(20),nullable=True)



class OrderPlaced(base):
    __tablename__="Oderpalced"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,ForeignKey("coustomerregister.id",ondelete='CASCADE'),nullable=False)
    product_id=Column(Integer,nullable=True)
    product_name=Column(String(200),nullable=True)
    product_quantity=Column(Integer,nullable=True)
    payment_mode=Column(String(200),nullable=False)
    order_status=Column(String(20),nullable=True)
    mrp=Column(Integer,nullable=True)
    discount_on_product=Column(Integer,nullable=True)
    total_price=Column(Integer,nullable=True)
    ordered_at=Column(TIMESTAMP,nullable=True)
    coustomer=relationship("Coustomer",back_populates="order",uselist=True)
    
class OtpManufacturer(base):
    __tablename__="Otpmanufacturer"
    id=Column(Integer,primary_key=True)
    email=Column(String(200),nullable=False)
    otp=Column(Integer,nullable=False)



class CoustomerProfile(base):
    __tablename__="coustomerprofile"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,ForeignKey("coustomerregister.id",ondelete='CASCADE'),nullable=False)
    coustomer_name=Column(String(20),nullable=True)
    address=Column(String(20),nullable=False)
    state=Column(String(200),nullable=False)
    pin_code=Column(Integer,nullable=False)
    coustomer=relationship("Coustomer",back_populates="profile")
    


class ManufacturerProfile(base):
    __tablename__="manufacturerprofile"
    id=Column(Integer,primary_key=True)
    manufacturer_id=Column(Integer,ForeignKey("manufacturersignup.id",ondelete='CASCADE'),nullable=False)
    store_name=Column(String(200),nullable=False)
    manufacturer_name=Column(String(20),nullable=True)
    email=Column(String(20),nullable=False)
    manufacturer=relationship("Manufacturer",back_populates="profile")
      

