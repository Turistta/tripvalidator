from datetime import datetime, time
from typing import Annotated, Dict, List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from models.base_models import Location


class ReviewAuthor(BaseModel):
    name: Annotated[str, Field(description="Name of the review author", examples=["João Paulo"])]
    profile_url: Annotated[
        Optional[HttpUrl],
        Field(
            default=None, description="URL to the author's profile", examples=["https://example.com/profile/joao_paulo"]
        ),
    ]
    email: Annotated[
        Optional[EmailStr], Field(default=None, description="Author's email address", examples=["joao@example.com"])
    ]


class Review(BaseModel):
    author: Annotated[ReviewAuthor, Field(description="Details of the review author")]
    rating: Annotated[float, Field(ge=0, le=5, description="Rating given by the author", examples=[4.5])]
    text: Annotated[str, Field(description="Content of the review", examples=["Great place, highly recommend!"])]
    language: Annotated[str, Field(max_length=2, description="Language code of the review", examples=["en"])]
    publication_time: Annotated[
        datetime, Field(description="Timestamp of when the review was published", examples=["2024-09-07T12:15:32.370Z"])
    ]


class Picture(BaseModel):
    url: Annotated[HttpUrl, Field(description="URL of the picture", examples=["https://example.com/picture.jpg"])]
    width: Annotated[int, Field(gt=0, description="Width of the picture in pixels", examples=[800])]
    height: Annotated[int, Field(gt=0, description="Height of the picture in pixels", examples=[600])]
    description: Annotated[
        Optional[str],
        Field(
            default=None, description="Optional description of the picture", examples=["A beautiful view of the park."]
        ),
    ]


class OpeningHours(BaseModel):
    monday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    tuesday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    wednesday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    thursday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    friday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    saturday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]
    sunday: Annotated[Optional[List[Dict[Literal["open", "close"], time]]], Field(default=None)]


class PlaceDetails(BaseModel):
    place_id: Annotated[
        str, Field(description="Unique identifier for the place", examples=["ChIJN7mK3OR4XpMRbkXk5ccxbKQ"])
    ]
    name: Annotated[str, Field(description="Name of the place", examples=["Parque Flamboyant"])]
    location: Annotated[Location, Field(description="Geographical location details of the place")]
    types: Annotated[
        List[str], Field(description="Categories that describe the place", examples=[["park", "tourist_attraction"]])
    ]
    reviews: Annotated[Optional[List[Review]], Field(default=None, description="List of user reviews for the place")]
    pictures: Annotated[List[Picture], Field(description="List of pictures of the place")]
    ratings_total: Annotated[int, Field(ge=0, description="Total number of ratings", examples=[12000])]
    opening_hours: Annotated[Optional[OpeningHours], Field(default=None, description="Opening hours of the place")]
