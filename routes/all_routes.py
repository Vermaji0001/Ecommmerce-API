from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session
from controller.coustomer import coutomer_register,coustomer_login
from controller.manufacturer import manufacturer_register,manufacturer_login,product_create
from schemas.userschemas import CoustomerRegisterSchemas,CoustomerLoginSchemas,ManufacturerRegisterSchemas,ManufacturerLoginSchemas,ProductCreateSchemas
from utils.get_db import get_db
from utils.function import manufacturer_data_by_token




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