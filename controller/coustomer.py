from fastapi import HTTPException

from modals.usermodal import Coustomer
from utils.function import hash_password,authanticate_coustomer,create_tokens,EXPIRY_MINUTES


from sqlalchemy.orm import Session


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
    

def coustomer_login(data,db:Session):
    coustomer=authanticate_coustomer(db,data.email,data.password)
    if not coustomer:
        raise HTTPException (status_code=404,detail="invalid detail")
    token=create_tokens(data={"sub":str(coustomer.id) },exipre=timedelta(minutes=EXPIRY_MINUTES))
    return {"msg":"sucessfully login",
            "user_id":coustomer.id,
            "coustomer_name":coustomer.coustomer_name,
            "token_url":token}
    
      

    





    


