from sqlalchemy.orm import Session
from fastapi import HTTPException
from modals.usermodal import Manufacturer,Category,Brand
from datetime import datetime,timedelta
from utils.function import hash_password
from utils.function import authanticate_manufacturer,create_tokens,EXPIRY_MINUTES





#register manufacturer 
special_crackter=["@","#","$","&"]

def manufacturer_register(data,db:Session):
    manufacturerdata=db.query(Manufacturer).filter(Manufacturer.store_name==data.store_name).first()
    if manufacturerdata:
        raise HTTPException (status_code=404,detail="your store name is already exists ")
    manufacturerdata=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if manufacturerdata:
        raise HTTPException (status_code=404,detail="your eamil is already exists")
    for cracker in special_crackter:
        if cracker in data.password:
            if len(data.password)>=8:
                hashpass=hash_password(data.password)
                time=datetime.now()
                manufact=Manufacturer(store_name=data.store_name,
                                      manufacturer_name=data.manufacturer_name,
                                      email=data.email,
                                      password=hashpass,
                                      created_at=time)
                db.add(manufact)
                db.commit()
                db.refresh(manufact)
                return {"msg":"Manufacturer register"}
            raise HTTPException (status_code=404,detail="your password length is less than 8")
        raise HTTPException (status_code=404,detail="use special cracker @,#,$,& in password")
    
    
#manufacturer login
def manufacturer_login(data,db:Session):
    manufacturer=authanticate_manufacturer(db,data.email,data.password)
    if not manufacturer:
        raise HTTPException(status_code=404,detail="invaild detail")
    token=create_tokens(data={"sub":str(manufacturer.id)},exipre=timedelta(minutes=EXPIRY_MINUTES))
    return {"msg":"Manufacturer login",
            "manufacturer_id":manufacturer.id,
            "manufacturer_name":manufacturer.manufacturer_name,
            "token":token}


def product_create(data,db:Session):
      manufacturer=db.query(Manufacturer).filter(Manufacturer.id==data.manufacturer_id).first()
      if not manufacturer:
           raise HTTPException (status_code=404,detail="Manufacturer id not match")
      discount_rupees=data.mrp*data.discount/100
      saleprice=data.mrp-discount_rupees
      manufact=Manufacturer(manufacturer_id=data.manufacturer_id,
                            product_name=data.product_name,
                            product_type=data.product_type,
                            category=data.category,
                            brand=data.brand,
                            mrp=data.mrp,
                            discount=data.discount,
                            sale_price=saleprice)
      db.add()(manufact)
      db.commit()
      db.refresh(manufact)
      xyz=Category(catergory_name=data.category)
      db.add(xyz)
      db.commit()
      db.refresh(xyz)
      new=Brand(brand_name=data.brand)
      db.add(new)
      db.commit()
      db.refresh(new)
      return {"msg":f"Product create id {manufacturer.id} and  product name is {data.product_name}"}





