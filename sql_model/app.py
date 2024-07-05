from sqlmodel import Field,SQLModel, Session, create_engine, select
from typing import Optional

class Hero(SQLModel, table=True):
    id: Optional[int]=Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int]= None
    team_id: Optional[int]= Field(default=None, foreign_key="team_id")

connection_string: str ="postgresql://SYED_NEON_PROJECT_owner:FGIuP37BZxHJ@ep-cold-flower-a1d4g6vm.ap-southeast-1.aws.neon.tech/sql_model_creatingtables?sslmode=require"
engine=create_engine(connection_string,echo=True)
def create_hero():
    hero1=Hero(name="syed sultan",secret_name="su")
    hero2=Hero(name="sultan",secret_name="su")
    hero3=Hero(name="syed ",secret_name="sy")
    session =Session(engine)
    session.add(hero1)
    session.add(hero2)
    session.add(hero3)
    session.commit()
    session.close()

def get_hero():
    session =Session(engine)
    statement=select(Hero).where(Hero.id==5)
    result=session.exec(statement)
    print(result.one())
    # for hero in result  :
    #     print("indvidiiuals")
    #     print(hero.name)

def update_hero():
    session= Session(engine)
    statement=select(Hero).where(Hero.name=="syed sultan")
    result=session.exec(statement).first()
    print(result)
    result.age=24  
    session.add(result)
    session.commit()
    print("updated data")
    print(result)
    session.close()

def delete_hero():
    session= Session(engine)
    statement=select(Hero).where(Hero.id==5)
    result=session.exec(statement).first()
    print(result)
    session.delete(result)
    session.commit()
    print("deleted data")
    session.close()




def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    # create_db_and_tables()
    # create_hero()
    # get_hero()
    #   update_hero()
        delete_hero()
    