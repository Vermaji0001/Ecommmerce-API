

from passlib.context import CryptContext
from datetime import datetime,timedelta
from modals.all_modals import Coustomer,Manufacturer
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from utils.get_db import get_db














password=CryptContext(schemes=["argon2"])

#create hash password
def hash_password(data:str):
    return password.hash(data)


#hash password verify
def varify_password(original_pass:str,hash_pass:str):
    return password.verify(original_pass,hash_pass)



#authanicate varification

def authanticate_coustomer(db:Session,email:str,password:str):
    user=db.query(Coustomer).filter(Coustomer.email==email).first()
    if not user:
        raise HTTPException (status_code=404,detail="not match your email id ")
    if not varify_password(password,user.password):
        raise HTTPException (status_code=404,detail="not match your password")
    return user


#authanthicate manufacturer
def authanticate_manufacturer(db:Session,email:str,password:str):
    user=db.query(Manufacturer).filter(Manufacturer.email==email).first()
    if not user:
        raise HTTPException (status_code=404,detail="not match your email id ")
    if not varify_password(password,user.password):
        raise HTTPException (status_code=404,detail="not match your password")
    return user

####################################################################################################################

#create token for coustomer login 


SECRET_KEY="YouAreLucky"
ALGORITHM="HS256"
EXPIRY_MINUTES=60*24


#create token function
def create_tokens(data:dict,exipre:Optional[timedelta]=None):
    userupdate=data.copy()
    if exipre:
       expire=datetime.now()+exipre
    else:
       exipre=datetime.now()+timedelta(minutes=EXPIRY_MINUTES) 
    userupdate.update({"exp":expire}) 
    token_url=jwt.encode(userupdate,SECRET_KEY,algorithm=ALGORITHM)
    return token_url
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="logintoken")


#get coustomer data by token
def coustomer_data_by_token(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
       
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        coustomer_id=payload.get("sub")
        
        if coustomer_id is None:
           raise HTTPException (status_code=404,detail="Not found  id data")
    except JWTError:
            raise HTTPException (status_code=404,detail="JWT error plaese check ")
    coustomer=db.query(Coustomer).filter(Coustomer.id==int(coustomer_id)).first()
    if not coustomer:
        raise HTTPException (status_code=404,detail="Not match your token id ")
    return coustomer





#get manufacturer data by token
def manufacturer_data_by_token(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
       
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        manufacturer_id=payload.get("sub")
        
        if manufacturer_id is None:
           raise HTTPException (status_code=404,detail="Not found  id data")
    except JWTError:
            raise HTTPException (status_code=404,detail="JWT error plaese check ")
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==int(manufacturer_id)).first()
    if not manufacturer:
        raise HTTPException (status_code=404,detail="Not match your token id ")
    return manufacturer



