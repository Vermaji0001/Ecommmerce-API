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
    product_quantity:int
    brand:str
    mrp:int
    discount:int
      
class OtpSentSchemas(BaseModel):
    email:str


class ResetPasswordSchemas(BaseModel):
    email:str
    otp:int
    new_password:str

class AddToCartSchemas(BaseModel):
    coustomer_id:int
    product_id:int
    product_quantity:int    

class OrderPlacedSchemas(BaseModel):
    coustomer_id:int 
    payment_mode:str  

class OrderCancelSchemas(BaseModel):
    coustomer_id:int 


class SentOptManufacturer(BaseModel):
    email:str



class ResetPasswordManufacturer(BaseModel):
    email:str
    otp:int
    new_password:str

class CoustomerProfileSchemas(BaseModel):
    coustomer_id:int    

class ManufacturerProfileSchemas(BaseModel):
    manufacturer_id:int   

class ChangeCoustomerDataSchemas(BaseModel):
    coustomer_id:int
    coustomer_name:str
    state:str
    address:str
    pin_code:int    

class ChangeManufacturerDataSchemas(BaseModel):
    manufacturer_id:int
    store_name:str
    manufacturer_name:str

class GetCoustomerProfile(BaseModel):
    coustomer_id:int    
        

class GetManufacturerProfile(BaseModel):
    manufacturer_id:int    
                

class GetAllProductManufacturer(BaseModel):
    manufacturer_id:int    
                                

class DeleteProduct(BaseModel):
    manufacturer_id:int
    delete_product:int

class GetproductByCategory(BaseModel):
    category:str


class GetproductByBrand(BaseModel):
    brand:str    