from ctypes.wintypes import POINT
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Annotated
class Herobase(SQLModel):
       name:str = Field(index=True)
       secret_name: str



class Hero(Herobase, table=True):
    id: int| None = Field(primary_key=True, default=None)
    age: int| None = None

class Heroupdate(SQLModel):
      name:str| None = None
      secret_name:str| None = None
      age: int| None = None


class HeroCreate(Herobase):

      age: int| None = None



class Heroresponse(Herobase):
     
      age: int| None = None

DB_URL ="postgresql://SYED_NEON_PROJECT_owner:FGIuP37BZxHJ@ep-cold-flower-a1d4g6vm.ap-southeast-1.aws.neon.tech/SQL_last?sslmode=require"
engine = create_engine('postgresql://SYED_NEON_PROJECT_owner:FGIuP37BZxHJ@ep-cold-flower-a1d4g6vm.ap-southeast-1.aws.neon.tech/SQL_last?sslmode=require')
def create_tables():
     SQLModel.metadata.create_all(engine)


app = FastAPI()


def get_deb():
     with Session(engine) as session:
          yield session
@app.on_event("startup")
def on_startup():
     create_tables()
@app.get("/")
async def root():
     return{"message":"Hello World"}

# get all heroes
@app.get("/heroes", response_model=list[Hero])
def get_heroes(session: Annotated[Session, Depends(get_deb)]):
     # with Session(engine) as session:
          heroes = session.exec(select(Hero)).all()
          return heroes 
     
# Create heroes
@app.post("/heroes")
def create_hero(hero:HeroCreate,db: Annotated[Session, Depends(get_deb)]):
     # with Session(engine) as session:
          print ("DATA FROM CLIENT", hero)
          hero_to_insert = Hero.model_validate(hero)
          print("DATA AFTER VALIDATION", hero_to_insert)
          db.add(hero_to_insert)
          db.commit()
          db.refresh(hero_to_insert)
          return hero_to_insert 


# single Hero
@app.get("/heroes/{hero_id}",response_model=Heroresponse)
def get_hero_by_id(hero_id: int,session:Annotated[Session, Depends(get_deb)]):
      hero =session.get(Hero,hero_id)
      if not hero:
             raise HTTPException(status_code=404, detail="Hero not found")
      return hero
# Hero update
@app.patch("/heroes/{hero_id}",response_model=Heroresponse)
def update_Hero(hero_id: int,hero_data: Heroupdate, session:Annotated[Session, Depends(get_deb)]):
      hero =session.get(Hero,hero_id)
      if not hero:
             raise HTTPException(status_code=404, detail="Hero not found")
      print("HERO IN DB",hero)
      print("DATA FROM CLIENT",hero_data)

      HERO_DICT_DATA = hero_data.model_dump(exclude_unset=True)
      print("HERO DICT",HERO_DICT_DATA)

      for key,value in HERO_DICT_DATA.items():
            setattr(hero,key,value)


      print("after", hero)
      Session.add(hero)
      session.commit()
      session.refresh(hero)
      return hero

# Hero delete