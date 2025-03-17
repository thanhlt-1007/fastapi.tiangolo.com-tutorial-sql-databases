from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Annotated

app = FastAPI()

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

class Hero(HeroBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    secret_name: str = Field()

class HeroPublic(HeroBase):
    id: int

class HeroCreate(HeroBase):
    secret_name: str

class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(url=sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/hello")
async def hello():
    return {
        "message": "Hello World"
    }

@app.get("/heroes")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@app.post("/heroes", response_model=HeroPublic)
async def create_hero(
    hero: HeroCreate,
    session: SessionDep,
) -> HeroPublic:
    db_herro = Hero.model_validate(hero)

    session.add(db_herro)
    session.commit()
    session.refresh(db_herro)
    return db_herro

@app.get("/heroes/{hero_id}")
async def read_heroes(
    hero_id: int,
    session: SessionDep,
) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.delete("/heroes/{hero_id}")
async def delete_hero(
    hero_id: int,
    session: SessionDep,
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"message": "Hero deleted successfully"}
