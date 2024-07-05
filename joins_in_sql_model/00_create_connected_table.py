from typing import Optional
from sqlmodel import Field, create_engine, SQLModel
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

def main():
    create_db_and_table()

if __name__ == "__main__":
    main()  