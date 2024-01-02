from sqlalchemy.orm import Session

import models
import schemas


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_movies(db: Session, skip: int = 0, limit: int = 10):
    movies = db.query(models.Movie).offset(skip).limit(limit).all()
    for movie in movies:
        movie.ratings = get_ratings_for_movie(db, movie.id)
    return movies


def get_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        movie.ratings = get_ratings_for_movie(db, movie_id)
    return movie


def create_movie_rating(db: Session, rating: schemas.RatingCreate, movie_id: int):
    db_rating = models.Rating(**rating.dict(), movie_id=movie_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_ratings_for_movie(db: Session, movie_id: int, skip: int = 0, limit: int = 10):
    ratings = db.query(models.Rating).filter(models.Rating.movie_id == movie_id).offset(skip).limit(limit).all()
    return ratings
