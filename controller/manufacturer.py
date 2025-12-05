from sqlalchemy.orm import Session
from fastapi import HTTPException
from modals.usermodal import Manufacturer,Category,Brand,Product,OtpManufacturer
from datetime import datetime,timedelta
from utils.function import hash_password
from utils.function import authanticate_manufacturer,create_tokens,EXPIRY_MINUTES
import random






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
      manufacturerxyz=db.query(Product).filter(Product.product_name==data.product_name).first()
      if   manufacturer and   manufacturerxyz :
           raise HTTPException (status_code=404,detail="Product is already reister by Manufacturer")
      discount_rupees=data.mrp*data.discount/100
      saleprice=data.mrp-discount_rupees
      manufact=Product(manufacturer_id=data.manufacturer_id,
                            product_name=data.product_name,
                            product_type=data.product_type,
                            category=data.category,
                            product_quantity=data.product_quantity,
                            brand=data.brand,
                            mrp=data.mrp,
                            discount_percentage=data.discount,
                            sale_price=saleprice)
      db.add(manufact)
      db.commit()
      category=db.query(Category).filter(Category.category_name==data.category).first()
      if not category:
           xyz=Category(category_name=data.category)
           db.add(xyz)
           db.commit()
           db.refresh(xyz)
      brand=db.query(Brand).filter(Brand.brand_name==data.brand).first()  
      if not brand :
            new=Brand(brand_name=data.brand)
            db.add(new)
            db.commit()
            db.refresh(new)
      return {"msg":"Product create "}

#Sent otp
def sent_otp_by_manufacturer(data,db:Session):
    otp=db.query(OtpManufacturer).filter(OtpManufacturer.email==data.email).first()
    if otp:
        raise HTTPException (status_code=404,detail="This Email otp already sent")
    manufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if not manufacturer:
        raise HTTPException (status_code=404,detail="invaild Email")
    otp=random.randint(1111,9999)
    xyz=OtpManufacturer(email=data.email,otp=otp)
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    return {"msg":f"sent otp this {data.email}",
            "email":data.email,
            "otp":otp}



# Coustmer reset password 
def reset_password_by_manufacturer(data,db:Session) :
        sentotp=db.query(OtpManufacturer).filter(OtpManufacturer.email==data.email).first()
        if not sentotp:
          raise HTTPException (status_code=404,detail="Not sent otp this email")
        if sentotp.otp==data.otp:
            for i in special_crackter:
                if i in data.new_password: 
                    if len(data.new_password)>=8:
                      hashpass=hash_password(data.new_password)
                      newdata=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
                      newdata.password=hashpass
                      db.commit()
                      db.refresh(newdata)
                      db.delete(sentotp)
                      db.commit()
                      db.refresh(newdata)
                      return {"msg":"Change your password"} 
                    raise HTTPException (status_code=404,detail="your password length is less than 8")
                raise HTTPException(status_code=404,detail="use special cracter @,#,$,& in password")   
        raise HTTPException(status_code=404,detail="invaild otp")    
      
