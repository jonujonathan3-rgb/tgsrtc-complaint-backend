from pydantic import BaseModel
from typing import Optional


class ComplaintCreate(BaseModel):

    name: str

    mobile: str

    email: Optional[str] = None


    bus_number: str

    journey_date: str

    journey_time: Optional[str] = None

    route: Optional[str] = None


    boarding_point: str

    destination: str


    category: str

    description: str