from fastapi import APIRouter,Depends,Query

from sqlalchemy.orm import Session
from controller.coustomer import coutomer_register,coustomer_login,sent_otp,reset_password_by_coustomer,show_all_category,show_all_brand,get_product_by_id,get_all_product_by_page,serach_product_by_name,add_to_cart,order_placed,order_cancel,create_profile_by_coustomer,change_coustomer_data,get_profile_by_coustomer,get_product_by_category,get_product_by_brand,get_order_by_coustomer,delete_coustomer,delete_add_to_cart,sort_coustomer

from schemas.coustomer_schemas import CoustomerRegisterSchemas,CoustomerLoginSchemas,OtpSentSchemas,ResetPasswordSchemas,AddToCartSchemas,OrderPlacedSchemas,OrderCancelSchemas,CoustomerProfileSchemas,ChangeCoustomerDataSchemas,GetCoustomerProfile,GetproductByCategory,GetproductByBrand,GetCoustomerOrder
from utils.get_db import get_db
from utils.function import coustomer_data_by_token




router=APIRouter()

#######################################################################################################################################################################


#Coustomer Register url

@router.post("/coustomerregister")
def coustomer_register_routes(data:CoustomerRegisterSchemas,db:Session=Depends(get_db)):
 final=coutomer_register(data,db)
 return final

#Coustomer Login url
@router.get("/coustomerlogin")
def login_coustomer(data:CoustomerLoginSchemas,db:Session=Depends(get_db)):
        user=coustomer_login(data,db)
        return user 


#Sent Otp
@router.post("/sentotp")
def otp_sent(data:OtpSentSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=sent_otp(data,db)
    return final

#Reset Passowrd
@router.patch("/resetpassword")
def password_reset(data:ResetPasswordSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=reset_password_by_coustomer(data,db)
    return final


#Get All Category
@router.get("/getallcategory")
def all_category(db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=show_all_category(db)
    return final



#Get All Brand
@router.get("/getallbrand")
def all_bramd(db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=show_all_brand(db)
    return final



#Get Product By Id 

@router.get("/getproduct/{id}")
def product_get_by_id(id:int,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=get_product_by_id(id,db)
    return final

#Get Product by Page to Page
@router.get("/getproductbypage")
def get_data_by_page(page:int=Query(1,ge=1),limit:int=Query(1,ge=1),db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=get_all_product_by_page(page,limit,db)
    return final


#Search Product
@router.get("/searchproduct")
def search_data_by_name(page:int=Query(1,ge=1),limit:int=Query(1,ge=1),name:str|None=None,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=serach_product_by_name(page,limit,name,db)
    return final


#Add to Cart
@router.post("/addtocart")
def add_cart(data:AddToCartSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=add_to_cart(data,db)
    return final

#Order Placed
@router.post("/orderplaced")
def placed_order(data:OrderPlacedSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=order_placed(data,db)
    return final


#order Cancel
@router.delete("/ordercancel")
def cencel_order(data:OrderCancelSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=order_cancel(data,db)
    return final





#Create Coustomer Profile
@router.post("/createprofilecoustomer")
def profile_create_bY_coustomer(data:CoustomerProfileSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=create_profile_by_coustomer(data,db)
    return final




#Change Coustomer Data
@router.patch("/changecoustomerdata")
def data_change_by_coustomer(data:ChangeCoustomerDataSchemas,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=change_coustomer_data(data,db)
    return final




#Get Coustomer Profile
@router.get("/getcoustomerprofile")
def coustomer_profile(data:GetCoustomerProfile,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=get_profile_by_coustomer(data,db)
    return final




#Get Product By Category
@router.get("/getproductbycategory")
def product_get_by_category(data:GetproductByCategory,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=get_product_by_category(data,db)
    return final


#Get Product By Brand
@router.get("/getproductbybrand")
def product_get_by_brand(data:GetproductByBrand,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=get_product_by_brand(data,db)
    return final




#Get All Order
@router.get("/getallorder")
def order_get(data:GetCoustomerOrder,db:Session=Depends(get_db),__=Depends(coustomer_data_by_token)):
    final=get_order_by_coustomer(data,db)
    return final


#Delete Coustomer 
@router.delete("/deletecoustomer/{id}")
def coustomer_delete(id:int,db:Session=Depends(get_db)):
    final=delete_coustomer(id,db)
    return final


#delete Cart

@router.delete("/deletecart/{id}")
def cart_delete(id:int,db:Session=Depends(get_db)):
    final=delete_add_to_cart(id,db)
    return final


#sort price

@router.get("/sort")
def sort_data(pricetype:str=Query("asc"),db:Session=Depends(get_db)):
    final=sort_coustomer(pricetype,db)
    return final

      


































