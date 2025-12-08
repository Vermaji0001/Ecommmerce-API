
from fastapi import FastAPI
from routes.coustomer_routes import router as coustomer_routes
from routes.manufacturer_routes import router as manufacturer_routes


from utils.get_db import engine,base


app=FastAPI()




app.include_router(coustomer_routes)
app.include_router(manufacturer_routes)

@app.on_event("startup")
def make_table():
    base.metadata.create_all(bind=engine)




  
                            



 










