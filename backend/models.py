from sqlalchemy import Column, Integer, String, Text

from .database import Base


class Complaint(Base):

    __tablename__ = "complaints"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    complaint_id = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )


    name = Column(
        String(100),
        nullable=False
    )


    mobile = Column(
        String(20),
        nullable=False
    )


    email = Column(
        String(150),
        nullable=True
    )


    bus_number = Column(
        String(50),
        nullable=False
    )


    journey_date = Column(
        String(20),
        nullable=False
    )


    journey_time = Column(
        String(50),
        nullable=True
    )


    route = Column(
        String(200),
        nullable=True
    )


    boarding_point = Column(
        String(150),
        nullable=False
    )


    destination = Column(
        String(150),
        nullable=False
    )


    category = Column(
        String(100),
        nullable=False
    )


    description = Column(
        Text,
        nullable=False
    )


    status = Column(
        String(50),
        default="Submitted"
    )


    submitted_at = Column(
        String(100),
        nullable=False
    )


    evidence_file = Column(
        String(255),
        nullable=True
    )