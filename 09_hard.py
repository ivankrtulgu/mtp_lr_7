from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from contextlib import asynccontextmanager

DATABASE_URL = "sqlite:///./09_hard.db"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/users")
async def read_users():
    query = "SELECT id, name FROM users"
    rows = await database.fetch_all(query)
    return [{"id": r["id"], "name": r["name"]} for r in rows]

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    query = "SELECT id, name FROM users WHERE id = :id"
    user = await database.fetch_one(query, values={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user["id"], "name": user["name"]}

@app.post("/users/{name}")
async def create_user(name: str):
    query = "INSERT INTO users (name) VALUES (:name)"
    user_id = await database.execute(query, values={"name": name})
    return {"id": user_id, "name": name}

@app.put("/users/{user_id}/{new_name}")
async def update_user(user_id: int, new_name: str):
    query_check = "SELECT id FROM users WHERE id = :id"
    user = await database.fetch_one(query_check, values={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    query = "UPDATE users SET name = :name WHERE id = :id"
    await database.execute(query, values={"name": new_name, "id": user_id})
    return {"id": user_id, "updated_name": new_name}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query_check = "SELECT id FROM users WHERE id = :id"
    user = await database.fetch_one(query_check, values={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    query = "DELETE FROM users WHERE id = :id"
    await database.execute(query, values={"id": user_id})
    return {"status": "deleted", "id": user_id}
