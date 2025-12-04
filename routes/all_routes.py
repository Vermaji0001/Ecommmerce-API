from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session
from controller.coustomer import coutomer_register,coustomer_login,sent_otp,reset_password_by_coustomer,show_all_category,show_all_brand
from controller.manufacturer import manufacturer_register,manufacturer_login,product_create
from schemas.userschemas import CoustomerRegisterSchemas,CoustomerLoginSchemas,ManufacturerRegisterSchemas,ManufacturerLoginSchemas,ProductCreateSchemas,OtpSentSchemas,ResetPasswordSchemas
from utils.get_db import get_db
from utils.function import manufacturer_data_by_token,coustomer_data_by_token




router=APIRouter()

#######################################################################################################################################################################


#coustomer register url

@router.post("/coustomerregister")
def coustomer_register_routes(data:CoustomerRegisterSchemas,db:Session=Depends(get_db)):
 final=coutomer_register(data,db)
 return final

#coustomer login url
@router.get("/coustomerlogin")
def login_coustomer(data:CoustomerLoginSchemas,db:Session=Depends(get_db)):
        user=coustomer_login(data,db)
        return user 

#manufacturer register
@router.post("/manufacturerregister")
def register_manu(data:ManufacturerRegisterSchemas,db:Session=Depends(get_db)):
    manu=manufacturer_register(data,db)
    return manu

#manufacturer login

@router.get("/manufacturerlogin")
def login_manufacturer(data:ManufacturerLoginSchemas,db:Session=Depends(get_db)):
    final=manufacturer_login(data,db)
    return final


#product create

@router.post("/productcreate")
def create_product(data:ProductCreateSchemas,db:Session=Depends(get_db),__=Depends(manufacturer_data_by_token)):
    final=product_create(data,db)
    return final

#sent otp
@router.post("/sentotp")
def otp_sent(data:OtpSentSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=sent_otp(data,db)
    return final

#reset passowrd
@router.patch("/resetpassword")
def password_reset(data:ResetPasswordSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=reset_password_by_coustomer(data,db)
    return final


#get all Category
@router.get("/getallcategory")
def all_category(db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=show_all_category(db)
    return final



#get all brand
@router.get("/getallbrand")
def all_bramd(db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=show_all_brand(db)
    return final
