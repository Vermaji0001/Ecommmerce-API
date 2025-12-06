from sqlalchemy.orm import Session
from fastapi import HTTPException
from modals.usermodal import Manufacturer,Category,Brand,Product,OtpManufacturer,ManufacturerProfile
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

xyz=0
def product_create(data,db:Session):
      profile=db.query(ManufacturerProfile).filter(ManufacturerProfile.manufacturer_id==data.manufacturer_id).first()
      if not profile:
          raise HTTPException(status_code=404,detail="Not create Product Without create Profile")
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
      
#create manufacturer profile

def create_profile_by_manufacturer(data,db:Session):
    profile=db.query(ManufacturerProfile).filter(ManufacturerProfile.manufacturer_id==data.manufacturer_id).first()
    if profile:
        raise HTTPException (status_code=404,detail="Already create profile this manufacturer")
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==data.manufacturer_id).first()
    if manufacturer:
        xyz=ManufacturerProfile(
                             manufacturer_id=data.manufacturer_id,
                             store_name=manufacturer.store_name,
                             manufacturer_name=manufacturer.manufacturer_name,
                             email=manufacturer.email,
                             )
        db.add(xyz)
        db.commit()
        db.refresh(xyz)
        return {"msg":"create your profile by manufacturer"}
    raise HTTPException(status_code=404,detail="manufacturer not register")




#change manufacturer data

def change_manufacturer_data(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==data.manufacturer_id).first()
    if manufacturer:
        manufacturer.store_name=data.store_name
        manufacturer.manufacturer_name=data.manufacturer_name
        db.commit()
        db.refresh(manufacturer)
        profile=db.query(ManufacturerProfile).filter(ManufacturerProfile.manufacturer_id==data.manufacturer_id).first()
        if profile:
            profile.store_name=data.store_name
            profile.manufacturer_name=data.manufacturer_name
            db.commit()
            db.refresh(profile)
            return {"msg":"change your data by manufacturer"}
        raise HTTPException(status_code=404,detail="Not match your profile id")
    raise HTTPException(status_code=404,detail="Not match your manufacturer id to manufacturer data")


#get profile by manufacturer

def get_profile_by_manufacturer(data,db:Session):
    profile=db.query(ManufacturerProfile).filter(ManufacturerProfile.manufacturer_id==data.manufacturer_id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="your not profile")
    return profile



#get all product by manufacturer

def get_all_product_by_manufacturer(data,db:Session):
    product=db.query(Product).filter(Product.manufacturer_id==data.manufacturer_id).all()
    if not product:
        raise HTTPException(status_code=404,detail="Not product This manufacturer")
    return product


#delete product by id

def delete_product_by_id(data,db:Session):
    product=db.query(Product).filter(Product.id==data.delete_product).first()
    if product:
        xyz=db.query(Product).filter(Product.manufacturer_id==data.manufacturer_id).first()
        db.delete(xyz)
        db.commit()
        
        return {"msg":"delete your product"}
    raise HTTPException(status_code=404,detail="invalid product  id")
    

    
        



