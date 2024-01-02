from pydantic import BaseModel


class RatingBase(BaseModel):
    rating: int


class RatingCreate(RatingBase):
    pass


class RatingUpdate(RatingBase):
    pass


class Rating(RatingBase):
    id: int
    movie_id: int

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    title: str
    release_year: int
    description: str
    budget: int
    duration: int


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    ratings: list[Rating] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
