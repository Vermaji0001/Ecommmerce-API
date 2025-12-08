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




class CoustomerProfileSchemas(BaseModel):
    coustomer_id:int    

 

class ChangeCoustomerDataSchemas(BaseModel):
    coustomer_id:int
    coustomer_name:str
    state:str
    address:str
    pin_code:int    



class GetCoustomerProfile(BaseModel):
    coustomer_id:int    
        
  
                
       


class GetproductByCategory(BaseModel):
    category:str


class GetproductByBrand(BaseModel):
    brand:str  



class GetCoustomerOrder(BaseModel):
    coustomer_id:int       



