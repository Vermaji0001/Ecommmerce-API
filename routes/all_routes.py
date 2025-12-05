from fastapi import APIRouter,Depends,Query

from sqlalchemy.orm import Session
from controller.coustomer import coutomer_register,coustomer_login,sent_otp,reset_password_by_coustomer,show_all_category,show_all_brand,get_product_by_id,get_all_product_by_page,serach_product_by_name,add_to_cart,order_placed,order_cancel
from controller.manufacturer import manufacturer_register,manufacturer_login,product_create,sent_otp_by_manufacturer,reset_password_by_manufacturer
from schemas.userschemas import CoustomerRegisterSchemas,CoustomerLoginSchemas,ManufacturerRegisterSchemas,ManufacturerLoginSchemas,ProductCreateSchemas,OtpSentSchemas,ResetPasswordSchemas,AddToCartSchemas,OrderPlacedSchemas,OrderCancelSchemas,SentOptManufacturer,ResetPasswordManufacturer
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



#get product by id 

@router.get("/getproduct/{id}")
def product_get_by_id(id:int,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=get_product_by_id(id,db)
    return final


@router.get("/getproductbypage")
def get_data_by_page(page:int=Query(1,ge=1),limit:int=Query(1,ge=1),db:Session=Depends(get_db)):
    final=get_all_product_by_page(page,limit,db)
    return final



@router.get("/searchproduct")
def search_data_by_name(page:int=Query(1,ge=1),limit:int=Query(1,ge=1),name:str|None=None,db:Session=Depends(get_db)):
    final=serach_product_by_name(page,limit,name,db)
    return final



@router.post("/addtocart")
def add_cart(data:AddToCartSchemas,db:Session=Depends(get_db)):
    final=add_to_cart(data,db)
    return final


@router.post("/orderplaced")
def placed_order(data:OrderPlacedSchemas,db:Session=Depends(get_db)):
    final=order_placed(data,db)
    return final



@router.delete("/ordercancel")
def cencel_order(data:OrderCancelSchemas,db:Session=Depends(get_db)):
    final=order_cancel(data,db)
    return final



@router.post("/sentotpmanufacturer")
def otp_sent_by_manufacturer(data:SentOptManufacturer,db:Session=Depends(get_db)):
    final=sent_otp_by_manufacturer(data,db)
    return final



@router.patch("/resetpasswordmanufacturer")
def password_reset_manufact(data:ResetPasswordManufacturer,db:Session=Depends(get_db)):
    final=reset_password_by_manufacturer(data,db)
    return final