from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from controller.manufacturer import manufacturer_register,manufacturer_login,product_create,sent_otp_by_manufacturer,reset_password_by_manufacturer,create_profile_by_manufacturer,change_manufacturer_data,get_profile_by_manufacturer,get_all_product_by_manufacturer,delete_product_by_id,product_data_change,delete_manufacturer
from schemas.manufacturer_schemas import ManufacturerRegisterSchemas,ManufacturerLoginSchemas,ProductCreateSchemas,SentOptManufacturer,ResetPasswordManufacturer,ManufacturerProfileSchemas,ChangeManufacturerDataSchemas,GetManufacturerProfile,GetAllProductManufacturer,DeleteProduct,ChangeProductData
from utils.get_db import get_db
from utils.function import manufacturer_data_by_token




router=APIRouter()







#Manufacturer Register
@router.post("/manufacturerregister")
def register_manu(data:ManufacturerRegisterSchemas,db:Session=Depends(get_db)):
    manu=manufacturer_register(data,db)
    return manu

#Manufacturer Login

@router.get("/manufacturerlogin")
def login_manufacturer(data:ManufacturerLoginSchemas,db:Session=Depends(get_db)):
    final=manufacturer_login(data,db)
    return final


#Product Create

@router.post("/productcreate")
def create_product(data:ProductCreateSchemas,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=product_create(data,db)
    return final



#Sent otp To Manufacturer
@router.post("/sentotpmanufacturer")
def otp_sent_by_manufacturer(data:SentOptManufacturer,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=sent_otp_by_manufacturer(data,db)
    return final


# varify Otp for Reset Password
@router.patch("/resetpasswordmanufacturer")
def password_reset_manufact(data:ResetPasswordManufacturer,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=reset_password_by_manufacturer(data,db)
    return final



#Ctreate Manufacturer Profile
@router.post("/createprofilemanufacturer")
def profile_create_by_manufacturer(data:ManufacturerProfileSchemas,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=create_profile_by_manufacturer(data,db)
    return final


#Get Manufacturer Profile
@router.get("/getmanufacturerprofile")
def manufacturer_profile(data:GetManufacturerProfile,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=get_profile_by_manufacturer(data,db)
    return final

#Change Product Data
@router.patch("/changeproductdata")
def change_product_data(data:ChangeProductData,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=product_data_change(data,db)
    return final


#Get All Product By Manufacturer
@router.get("/getallproductmanufacturer")
def get_all_product_manufacturer(data:GetAllProductManufacturer,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=get_all_product_by_manufacturer(data,db)
    return final

# Delete Product By Manufacturer
@router.delete("/deleteproduct")
def product_delete(data:DeleteProduct,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=delete_product_by_id(data,db)
    return final

# Change Manufacturer Data
@router.patch("/changemanufacturerdata")
def manufacturer_data_change(data:ChangeManufacturerDataSchemas,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=change_manufacturer_data(data,db)
    return final


#delete Manufacturer
@router.delete("/deletemanufacturer/{id}")
def manufacturer_delete(id:int,db:Session=Depends(get_db)):
    final=delete_manufacturer(id,db)
    return final