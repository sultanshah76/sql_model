
from typing import Optional
from sqlalchemy import select
from sqlmodel import Field, Session, create_engine, SQLModel
from dotenv import load_dotenv, find_dotenv
from os import getenv

_:bool= load_dotenv(find_dotenv())

class Team(SQLModel, table=True):
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
        team_avengers = Team(name= "avengers", headquaters="avengers tower",id=1)
        team_justice_league = Team(name= "justice League", headquaters="hall of justice",id=2)
        session.add(team_avengers)
        session.add(team_justice_league)    
        session.commit()

        hero_superman = Hero(name="clark kent", secret_name="Superman",age=32, team_id=team_avengers.id)
        hero_spiderman = Hero(name="peter parker", secret_name="Spiderman",age=30)
        hero_batman = Hero(name="bruce wayne", secret_name="Batman", team_id=team_avengers.id)
        session.add(hero_superman)
        session.add(hero_spiderman)
        session.add(hero_batman)
        session.commit()


def select_heros_by_where():
    with Session(engine)as session:
        statement=select(Hero).where(Hero.team_id == 1)
        result= session.exec(statement).all()
        heroes= result
        print("Heroes", heroes)


def select_hero_by_join():
    with Session(engine)as session:
        statement=select(Hero).join(Team)
        result= session.exec(statement)
        heroes= result.all()
        print("Heroes", heroes)
  

def select_hero_by_left_join():
     with Session(engine)as session:
        statement=select(Hero).join(Team,isouter=True)
        result= session.exec(statement)
        heroes= result.all()
        print("Heroes", heroes)


def select_hero_by_Right_join():
     with Session(engine)as session:
        statement=select(Team).join(Hero,isouter=True)
        result= session.exec(statement)
        heroes= result.all()
        print("Heroes", heroes)


def select_hero_by_full_join():
     with Session(engine)as session:
        statement=select(Hero).join(Team,full=True)
        result= session.exec(statement)
        heroes= result.all()
        print("Heroes", heroes)        




def main():
    # create_db_and_table()
    # create_heroes()
    #  select_heros_by_where()
     select_hero_by_join()
    #  select_hero_by_left_join()
    # select_hero_by_Right_join()
    # select_hero_by_full_join()

if __name__ == "__main__":
    
    main()  