from pydantic import BaseModel



class CoustomerRegisterSchemas(BaseModel):
    coustomer_name:str
    email:str
    password:str
    state:str
    address:str
    pincode:int


class CoustomerLoginSchemas(BaseModel):
    email:str
    password:str



class ManufacturerRegisterSchemas(BaseModel):
    store_name:str
    manufacturer_name:str
    email:str
    password:str


class ManufacturerLoginSchemas(BaseModel):
    email:str
    password:str


class ProductCreateSchemas(BaseModel):
    manufacturer_id:int
    product_name:str
    product_type:str
    category:str
    brand:str
    mrp:int
    discount:int
      
class OtpSentSchemas(BaseModel):
    email:str


class ResetPasswordSchemas(BaseModel):
    email:str
    otp:int
    new_password:str