from pydantic import BaseModel



##############################################################################################################################################################################################        




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
    discount_percentage:int


class SentOptManufacturer(BaseModel):
    email:str



class ResetPasswordManufacturer(BaseModel):
    email:str
    otp:int
    new_password:str



class ManufacturerProfileSchemas(BaseModel):
    manufacturer_id:int  



class ChangeManufacturerDataSchemas(BaseModel):
    manufacturer_id:int
    store_name:str
    manufacturer_name:str    




class GetManufacturerProfile(BaseModel):
    manufacturer_id:int      




class GetAllProductManufacturer(BaseModel):
    manufacturer_id:int    
                             



class DeleteProduct(BaseModel):
    manufacturer_id:int
    delete_product:int                             


class ChangeProductData(BaseModel):
    manufacturer_id:int
    product_id:int
    product_name:str
    product_type:str
    category:str
    product_quantity:int
    brand:str
    mrp:int
    discount:int      