from typing import Optional, List, ForwardRef
from sqlmodel import Field, Relationship, Session, select, create_engine, SQLModel
from dotenv import load_dotenv, find_dotenv
from os import getenv

# Load environment variables
_: bool = load_dotenv(find_dotenv())

# # Forward declarations
# Hero = ForwardRef('Hero')

class Team(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    headquaters: str
    heros: List['Hero'] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heros")

joins_url = getenv("sql_model_Joins")
engine = create_engine(joins_url, echo=True)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    with Session(engine) as session:
        statement1 = select(Team).where(Team.name == "airfighters")
        bella = session.exec(statement1).first()
        statement = select(Hero).where(Hero.secret_name == "belfiore")
        hero = session.exec(statement).first()
        hero.team =bella
        session.add(hero)
        session.commit()
def create_new_hero_and_teams():
    with Session(engine) as session:
        hero_black_lion = Hero(name="black lion", secret_name="trevor challa", age=30)
        hero_pink_lion = Hero(name="pink lion", secret_name="trimming center")
        team2 = Team(name="marvel", headquaters="Washington D.C.")
        team2.heros = [hero_pink_lion, hero_black_lion]
        session.add(team2)
        session.commit()
def main():
    # create_db_and_table()
    # create_heroes()
    create_new_hero_and_teams()

if __name__ == "__main__":
    main()
