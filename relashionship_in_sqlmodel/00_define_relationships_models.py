from typing import Optional, List, ForwardRef
from sqlmodel import Field, Relationship, Session, create_engine, SQLModel
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
        team_fighters = Team(name="airfighters", headquaters="airfighters tower")
        team_moon = Team(name="justice moons", headquaters="hall of moon")

        hero_1 = Hero(name="clark kent", secret_name="Superman", team=team_fighters)
        hero_2 = Hero(name="bruce wayne", secret_name="Batman", team=team_fighters)
        hero_3 = Hero(name="peter parker", secret_name="belfiore", team=team_moon)
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()

def main():
    create_db_and_table()
    create_heroes()

if __name__ == "__main__":
    main()
