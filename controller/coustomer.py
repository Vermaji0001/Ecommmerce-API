from fastapi import HTTPException

from modals.usermodal import Coustomer,Otp,Category,Brand
from utils.function import hash_password,authanticate_coustomer,create_tokens,EXPIRY_MINUTES


from sqlalchemy.orm import Session

import random
from datetime import datetime,timedelta



   




#Coutomer register 
special_crackter=["@","#","$","&"]

def coutomer_register(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if coustomer:
        raise HTTPException (status_code=404,detail="Your email is already exists")
    for crackter in special_crackter:
        if crackter in data.password:
              if len(data.password)>=8 :
                 hashpass=hash_password(data.password)
                 time=datetime.now()
                 user=Coustomer(coustomer_name=data.coustomer_name,
                                email=data.email,
                                password=hashpass,
                                state=data.state,
                                address=data.address,
                                pincode=data.pincode,
                                created_at=time)
                 db.add(user)
                 db.commit()
                 db.refresh(user)
                 return {"msg":"Coustomer is Regsiter "}
              raise HTTPException (status_code=404,detail="Your Password length is less than 8")
        raise HTTPException ( status_code=404,detail="Please use Special Crackter @,#,$,&")
    
#coustomer login
def coustomer_login(data,db:Session):
    coustomer=authanticate_coustomer(db,data.email,data.password)
    if not coustomer:
        raise HTTPException (status_code=404,detail="invalid detail")
    token=create_tokens(data={"sub":str(coustomer.id) },exipre=timedelta(minutes=EXPIRY_MINUTES))
    return {"msg":"sucessfully login",
            "user_id":coustomer.id,
            "coustomer_name":coustomer.coustomer_name,
            "token_url":token}


def sent_otp(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if not coustomer:
        raise HTTPException (status_code=404,detail="invaild Email")
    otp=random.randint(1111,9999)
    xyz=Otp(email=data.email,otp=otp)
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    return {"msg":"sent otp",
            "email":data.email,
            "otp":otp}




# coustmer reset password 
def reset_password_by_coustomer(data,db:Session) :
        coustomer=db.query(Otp).filter(Otp.email==data.email).first()
        if not coustomer:
          raise HTTPException (status_code=404,detail="Not sent otp this email")
        if coustomer.otp==data.otp:
            for i in special_crackter:
                if i in data.new_password: 
                    if len(data.new_password)>=8:
                      hashpass=hash_password(data.new_password)
                      newdata=db.query(Coustomer).filter(Coustomer.email==data.email).first()
                      newdata.password=hashpass
                      db.commit()
                      db.refresh(newdata)
                      db.delete(coustomer)
                      return {"msg":"Change your password"} 
                    raise HTTPException (status_code=404,detail="your password length is less than 8")
                raise HTTPException(status_code=404,detail="use special cracter @,#,$,& in password")   
        raise HTTPException(status_code=404,detail="invaild otp")    
      



#show all category of coustomer
def show_all_category(db:Session):
    category=db.query(Category).all()
    return category
    
#show all brand pf coustomer
def show_all_brand(db:Session):
    brand=db.query(Brand).all()
    return brand
    



    


