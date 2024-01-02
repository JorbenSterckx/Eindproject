import secrets

from fastapi import Depends, FastAPI, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import os
import crud
import models
import schemas
from database import SessionLocal, engine

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBasic()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db=db, movie=movie)


@app.get("/movies/", response_model=list[schemas.Movie])
def list_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_movies(db, skip=skip, limit=limit)


@app.post("/movies/{movie_id}/ratings/", response_model=schemas.Rating)
def create_movie_rating(movie_id: int, rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    return crud.create_movie_rating(db=db, rating=rating, movie_id=movie_id)


@app.get("/movies/{movie_id}/ratings/", response_model=list[schemas.Rating])
def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    return crud.get_ratings_for_movie(db, movie_id)


@app.delete("/movies/{movie_id}/ratings/{rating_id}", response_model=schemas.Rating)
def delete_rating_from_movie(movie_id: int, rating_id: int, db: Session = Depends(get_db)):
    db_rating = db.query(models.Rating).filter(
        models.Rating.movie_id == movie_id,
        models.Rating.id == rating_id
    ).first()

    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(db_rating)
    db.commit()
    return db_rating


@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    return crud.get_movie(db, movie_id)


@app.put("/ratings/{rating_id}", response_model=schemas.Rating)
def update_rating(rating_id: int, rating_data: schemas.RatingUpdate, db: Session = Depends(get_db)):
    db_rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()

    if db_rating:
        for key, value in rating_data.dict().items():
            setattr(db_rating, key, value)

        db.commit()
        db.refresh(db_rating)
        return db_rating
    else:
        raise HTTPException(status_code=404, detail="Rating not found")
