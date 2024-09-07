from datetime import datetime, time
from typing import Annotated, Dict, List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from models.base_models import Location


class ReviewAuthor(BaseModel):
    name: Annotated[str, Field()]
    profile_url: Annotated[Optional[HttpUrl], Field(default=None)]
    email: Annotated[Optional[EmailStr], Field(default=None)]


class Review(BaseModel):
    author: Annotated[ReviewAuthor, Field()]
    rating: Annotated[float, Field(ge=0, le=5)]
    text: Annotated[str, Field()]
    language: Annotated[str, Field(max_length=2)]
    publication_time: Annotated[datetime, Field()]


class Picture(BaseModel):
    url: Annotated[HttpUrl, Field()]
    width: Annotated[int, Field(gt=0)]
    height: Annotated[int, Field(gt=0)]
    description: Annotated[Optional[str], Field(default=None)]


class OpeningHours(BaseModel):
    monday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    tuesday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    wednesday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    thursday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    friday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    saturday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    sunday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]


class PlaceDetails(BaseModel):
    place_id: Annotated[str, Field()]
    name: Annotated[str, Field()]
    location: Annotated[Location, Field()]
    types: Annotated[List[str], Field()]
    reviews: Annotated[Optional[List[Review]], Field()]
    pictures: Annotated[List[Picture], Field()]
    ratings_total: Annotated[int, Field(ge=0)]
    opening_hours: Annotated[Optional[OpeningHours], Field(default=None)]
