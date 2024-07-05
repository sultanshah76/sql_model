from typing import Optional
from sqlmodel import Field, Session, create_engine, SQLModel
from dotenv import load_dotenv, find_dotenv
from os import getenv

_:bool= load_dotenv(find_dotenv())

class team(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    headquaters: str

class Hero(SQLModel, table=True):
    id: Optional[int]=Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int]= None
    team_id: Optional[int]= Field(default=None, foreign_key="team.id")



joins_url= getenv("sql_model_Joins")
engine=create_engine(joins_url,echo=True)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    with Session(engine) as session:
        team_avengers = team(name= "avengers", headquaters="avengers tower",id=1)
        team_justice_league = team(name= "justice League", headquaters="hall of justice",id=2)
        session.add(team_avengers)
        session.add(team_justice_league)   
        session.commit()

        hero_superman = Hero(name="clark kent", secret_name="Superman",age=32, team_id=team_avengers.id)
        hero_batman = Hero(name="bruce wayne", secret_name="Batman", team_id=team_avengers.id)
        hero_spiderman = Hero(name="peter parker", secret_name="Spiderman",age=30)
        session.add(hero_superman)
        session.add(hero_spiderman)
        session.add(hero_batman)
        session.commit()


  






def main():
    # create_db_and_table()
    create_heroes()

if __name__ == "__main__":
    main()  