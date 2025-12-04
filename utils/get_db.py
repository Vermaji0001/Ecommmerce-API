
from sqlalchemy.orm import Session,sessionmaker,declarative_base

from sqlalchemy import create_engine


#code connect with data base
DATABASE_URL=DATABASE_URL="postgresql+psycopg2://postgres:Prince@localhost/instagramwithdatabase"
engine=create_engine(DATABASE_URL,echo=True)
sessionlocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
base=declarative_base()


def get_db():
    db:Session=sessionlocal()
    try:
        yield db
    finally:
        db.close()

################################################################################################################################
