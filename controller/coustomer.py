from fastapi import HTTPException,Query

from modals.usermodal import Coustomer,Otp,Category,Brand,Product,AddToCart,OrderPlaced,CoustomerProfile
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
    
#Coustomer login
def coustomer_login(data,db:Session):
    coustomer=authanticate_coustomer(db,data.email,data.password)
    if not coustomer:
        raise HTTPException (status_code=404,detail="invalid details")
    token=create_tokens(data={"sub":str(coustomer.id) },exipre=timedelta(minutes=EXPIRY_MINUTES))
    return {"msg":"sucessfully login",
            "user_id":coustomer.id,
            "coustomer_name":coustomer.coustomer_name,
            "token_url":token}


#Sent otp
def sent_otp(data,db:Session):
    otp=db.query(Otp).filter(Otp.email==data.email).first()
    if otp:
        raise HTTPException (status_code=404,detail="On This Email otp already sent")
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if not coustomer:
        raise HTTPException (status_code=404,detail="invaild Email")
    otp=random.randint(1111,9999)
    xyz=Otp(email=data.email,otp=otp)
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    return {"msg":f"sent otp this {data.email}",
            "email":data.email,
            "otp":otp}




# Coustmer reset password 
def reset_password_by_coustomer(data,db:Session) :
        coustomer=db.query(Otp).filter(Otp.email==data.email).first()
        if not coustomer:
          raise HTTPException (status_code=404,detail="Please sent Otp")
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
      



#Show all category of coustomer
def show_all_category(db:Session):
    category=db.query(Category).all()
    return category
    
#Show all brand of coustomer
def show_all_brand(db:Session):
    brand=db.query(Brand).all()
    return brand
    



#Get product by product id 

def get_product_by_id(id,db:Session):
    product=db.query(Product).filter(Product.id==id).first()
    if product:
        return product
    raise HTTPException(status_code=404,detail="Not avialable this product")


#Get product  data according to page 
def get_all_product_by_page(page:Query,limit:Query,db:Session):
    product=db.query(Product)
    skip=int((page-1)*limit)
    xyz=product.offset(skip).limit(limit).all()
    return {"msg":"your data",
                "limit":limit,
                "data":xyz}



#Search product by product name
def serach_product_by_name(limit,page,name,db:Session):
    data=db.query(Product)
    if name:
        final=data.filter(Product.product_name.ilike(f"%{name}%"))
    skip=int((page-1)*limit)
    userdata=final.offset(skip).limit(limit).all()
    return {"pageno":page,
    "limit":limit,
    "data":userdata}  



#Add to Cart
def add_to_cart(data,db:Session):
    profile=db.query(CoustomerProfile).filter(CoustomerProfile.coustomer_id==data.coustomer_id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="create profile before add to cart")
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise  HTTPException(status_code=404,detail="invalid coustomer id ")
    product=db.query(Product).filter(Product.id==data.product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="product not avialable")
    if product.product_quantity :
        xyz=AddToCart(coustomer_id=data.coustomer_id,product_id=data.product_id,product_quantity=data.product_quantity)
        db.add(xyz)
        db.commit()
        db.refresh(xyz)
        return {"msg":"Product add to cart "}
    raise HTTPException(status_code=404,detail="out of stock")





#Oder Placed

oder_done="your order is done "
payment_mode=["Cash on delivery","upi"]
def order_placed(data,db:Session):
    coustomer=db.query(AddToCart).filter(AddToCart.coustomer_id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="please add to cart")
    product=db.query(Product).filter(Product.id==coustomer.product_id).first()
    if not product:
         raise HTTPException(status_code=404,detail="inalvid ")
    for i in payment_mode:
        if i==data.payment_mode:
               totalprice=coustomer.product_quantity*product.sale_price
               time=datetime.now()
               discount_value=product.mrp*product.discount_percentage/100
               discount_on_one_product=product.mrp-discount_value
               xyz=OrderPlaced(coustomer_id=data.coustomer_id,
                               product_id=coustomer.product_id,
                               product_name=product.product_name,
                               product_quantity=coustomer.product_quantity,
                               payment_mode=data.payment_mode,
                               order_status=oder_done,
                               mrp=product.mrp,
                               discount_on_product=discount_on_one_product,
                               total_price=totalprice,
                               ordered_at=time)
               db.add(xyz)
               db.commit()
               db.refresh(xyz)
               db.delete(coustomer)
               xyz=product.product_quantity-coustomer.product_quantity
               product.product_quantity=xyz
               db.commit()
               return {"msg":" OrderPlaced THank YOu",
                       "Product_name":product.product_name,
                       "payment_mode":data.payment_mode,
                       "Oder_Status":oder_done,
                       "MRP":product.mrp,
                       "Discount_On_Product":discount_value,
                       "Product_Quantity":coustomer.product_quantity,
                       "Total_price":totalprice}
    raise HTTPException(status_code=404,detail="Choose Payment Mode from in Cash on delivery or  upi")
    
    

#order cancel
def order_cancel(data,db:Session):
    coustomer=db.query(OrderPlaced).filter(OrderPlaced.coustomer_id==data.coustomer_id).first()
    if coustomer:
        product=db.query(Product).filter(Product.id==coustomer.product_id).first()
        if product:
            product.product_quantity+=coustomer.product_quantity
            db.commit()
            db.delete(coustomer)
            
            return {"msg":f"Delete your order {coustomer.product_id}"}
        raise HTTPException(status_code=404,detail="invalid product id ")
    raise HTTPException(status_code=404,detail="Your not order")
        


#create profile
def create_profile_by_coustomer(data,db:Session):
    profile=db.query(CoustomerProfile).filter(CoustomerProfile.coustomer_id==data.coustomer_id).first()
    if profile:
        raise HTTPException (status_code=404,detail="Already create profile this coustomer")
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if coustomer:
        xyz=CoustomerProfile(coustomer_id=data.coustomer_id,
                             coustomer_name=coustomer.coustomer_name,
                             address=coustomer.address,
                             state=coustomer.state,
                             pin_code=coustomer.pincode)
        db.add(xyz)
        db.commit()
        db.refresh(xyz)
        return {"msg":"create your profile"}
    raise HTTPException(status_code=404,detail="Coustomer not register")




#change coustomer data 
def change_coustomer_data(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if coustomer:
        coustomer.coustomer_name=data.coustomer_name   #change data in coustomer table
        coustomer.state=data.state
        coustomer.address=data.address
        coustomer.pincode=data.pin_code
        db.commit()
        db.refresh(coustomer)
        profile=db.query(CoustomerProfile).filter(CoustomerProfile.coustomer_id==data.coustomer_id).first() 
        if profile:
           profile.coustomer_name=data.coustomer_name                           #change data in cosutomer profile
           profile.state=data.state
           profile.address=data.address
           profile.pin_code=data.pin_code
           db.commit()
           db.refresh(profile)
           return{"msg":"change your coustomer data"}
        raise HTTPException(status_code=404,detail="not match coustomer id to profile")
    raise HTTPException(status_code=404,detail="Not coustomer")
    



#get profile by coustomer

def get_profile_by_coustomer(data,db:Session):
    profile=db.query(CoustomerProfile).filter(CoustomerProfile.coustomer_id==data.coustomer_id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="your not profile")
    return profile


#get_product_by category
def get_product_by_category(data,db:Session):
    product=db.query(Product).filter(Product.category==data.category).all()
   
    if not product:
        raise HTTPException(status_code=404,detail=f"this  is wrong category")
    return product


#get product by brand

def get_product_by_brand(data,db:Session):
    product=db.query(Product).filter(Product.brand==data.brand).all()
    if not product:
        raise HTTPException(status_code=404,detail="this  is wrong brand")
    return product

#get odrder by coustomer

def get_order_by_coustomer(data,db:Session):
    order=db.query(OrderPlaced).filter(OrderPlaced.coustomer_id==data.coustomer_id).all()
    if not order:
        raise HTTPException(status_code=404,detail="Your Not Order")
    return order


#delete Costomer

def delete_coustomer(id,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==id).first()
    if coustomer:
        db.delete(coustomer)
        db.commit()
        return {"msg":f"Delete your coustomer {id} "}
    raise HTTPException(status_code=404,detail="invaild Coustomer id ")