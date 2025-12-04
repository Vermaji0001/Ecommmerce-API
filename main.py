
from fastapi import FastAPI
from routes.all_routes import router


from utils.get_db import engine,base


app=FastAPI()




app.include_router(router)

@app.on_event("startup")
def make_table():
    base.metadata.create_all(bind=engine)




  
                            



 










