from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import random
import os
import shutil

from .database import engine, Base, get_db
from .models import Complaint
from .schemas import ComplaintCreate


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# CREATE FASTAPI APP
# =====================================================

app = FastAPI(
    title="TGSRTC Complaint Portal API",
    description="Backend API for the student complaint portal prototype",
    version="1.0.0"
)
# =====================================================
# FILE UPLOAD CONFIGURATION
# =====================================================

UPLOAD_BASE_DIR = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

IMAGE_UPLOAD_DIR = os.path.join(
    UPLOAD_BASE_DIR,
    "images"
)

VIDEO_UPLOAD_DIR = os.path.join(
    UPLOAD_BASE_DIR,
    "videos"
)

os.makedirs(
    IMAGE_UPLOAD_DIR,
    exist_ok=True
)


os.makedirs(
    VIDEO_UPLOAD_DIR,
    exist_ok=True
)
# =====================================================
# SERVE UPLOADED EVIDENCE FILES
# =====================================================

app.mount(
    "/uploads/images",
    StaticFiles(directory=IMAGE_UPLOAD_DIR),
    name="uploaded_images"
)

app.mount(
    "/uploads/videos",
    StaticFiles(directory=VIDEO_UPLOAD_DIR),
    name="uploaded_videos"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://127.0.0.1:5500",
        "http://localhost:5500",

        # GitHub Pages frontend
        "https://jonujonathan3-rgb.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# BASIC ROUTES
# =====================================================

@app.get("/")
def root():

    return {
        "message": "TGSRTC Complaint Portal Backend is running!"
    }


@app.get("/api/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/api/database")
def database_status():

    return {
        "database": "SQLite",
        "status": "connected"
    }


# =====================================================
# GENERATE COMPLAINT ID
# =====================================================

def generate_complaint_id():

    today = datetime.now().strftime("%Y%m%d")

    random_number = random.randint(1000, 9999)

    return f"TGSRTC-{today}-{random_number}"


# =====================================================
# CREATE COMPLAINT
# =====================================================
@app.post("/api/complaints")
async def create_complaint(
    name: str = Form(...),
    mobile: str = Form(...),
    email: str = Form(""),
    bus_number: str = Form(...),
    journey_date: str = Form(...),
    journey_time: str = Form(""),
    route: str = Form(""),
    boarding_point: str = Form(...),
    destination: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    evidence: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):

    complaint_id = generate_complaint_id()

    while db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first():

        complaint_id = generate_complaint_id()


    evidence_filename = None


    if evidence and evidence.filename:

        filename = evidence.filename

        extension = os.path.splitext(
            filename
        )[1].lower()


        image_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        ]

        video_extensions = [
            ".mp4",
            ".mov",
            ".webm"
        ]


        if extension in image_extensions:

            upload_dir = IMAGE_UPLOAD_DIR

        elif extension in video_extensions:

            upload_dir = VIDEO_UPLOAD_DIR

        else:

            raise HTTPException(
                status_code=400,
                detail="Unsupported evidence file type."
            )


        evidence_filename = (
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}_"
            f"{random.randint(1000,9999)}"
            f"{extension}"
        )


        file_path = os.path.join(
            upload_dir,
            evidence_filename
        )


        try:

            with open(
                file_path,
                "wb"
            ) as buffer:

                shutil.copyfileobj(
                    evidence.file,
                    buffer
                )

        except Exception as error:

            print(
                "Evidence upload error:",
                error
            )

            raise HTTPException(
                status_code=500,
                detail="Unable to save evidence file."
            )


    new_complaint = Complaint(

        complaint_id=complaint_id,

        name=name,

        mobile=mobile,

        email=email or None,

        bus_number=bus_number,

        journey_date=journey_date,

        journey_time=journey_time or None,

        route=route or None,

        boarding_point=boarding_point,

        destination=destination,

        category=category,

        description=description,

        status="Submitted",

        submitted_at=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        evidence_file=evidence_filename
    )


    db.add(new_complaint)

    db.commit()

    db.refresh(new_complaint)


    return {

        "message":
            "Complaint submitted successfully",

        "complaint_id":
            new_complaint.complaint_id,

        "status":
            new_complaint.status,

        "evidence_file":
            new_complaint.evidence_file
    }
@app.get("/api/complaints/{complaint_id}")
def get_complaint(
    complaint_id: str,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    return {
        "complaint_id": complaint.complaint_id,
        "name": complaint.name,
        "mobile": complaint.mobile,
        "email": complaint.email,
        "bus_number": complaint.bus_number,
        "journey_date": complaint.journey_date,
        "journey_time": complaint.journey_time,
        "route": complaint.route,
        "boarding_point": complaint.boarding_point,
        "destination": complaint.destination,
        "category": complaint.category,
        "description": complaint.description,
        "status": complaint.status,
        "submitted_at": complaint.submitted_at,
        "evidence_file": complaint.evidence_file
    }
@app.get("/api/complaints")
def get_all_complaints(
    db: Session = Depends(get_db)
):

    complaints = db.query(Complaint).order_by(
        Complaint.id.desc()
    ).all()


    return [
        {
            "complaint_id": complaint.complaint_id,
            "name": complaint.name,
            "mobile": complaint.mobile,
            "email": complaint.email,
            "bus_number": complaint.bus_number,
            "journey_date": complaint.journey_date,
            "journey_time": complaint.journey_time,
            "route": complaint.route,
            "boarding_point": complaint.boarding_point,
            "destination": complaint.destination,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "submitted_at": complaint.submitted_at,
            "evidence_file": complaint.evidence_file
        }
        for complaint in complaints
    ]


@app.put("/api/complaints/{complaint_id}/status")
def update_complaint_status(
    complaint_id: str,
    status_data: dict,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    new_status = status_data.get("status")

    allowed_statuses = [
        "Submitted",
        "Under Review",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid complaint status"
        )

    complaint.status = new_status

    db.commit()
    db.refresh(complaint)

    return {
        "message": "Complaint status updated successfully",
        "complaint_id": complaint.complaint_id,
        "status": complaint.status
    }
# =====================================================
# EVIDENCE FILE UPLOAD
# =====================================================

@app.post("/api/upload-evidence")
async def upload_evidence(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    filename = file.filename

    extension = os.path.splitext(
        filename
    )[1].lower()

    image_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    video_extensions = [
        ".mp4",
        ".mov",
        ".webm"
    ]

    if extension in image_extensions:

        upload_dir = IMAGE_UPLOAD_DIR

    elif extension in video_extensions:

        upload_dir = VIDEO_UPLOAD_DIR

    else:

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

    safe_filename = (
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}_"
        f"{random.randint(1000,9999)}"
        f"{extension}"
    )

    file_path = os.path.join(
        upload_dir,
        safe_filename
    )

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as error:

        print(
            "File upload error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to save uploaded file."
        )

    return {
        "message": "File uploaded successfully",
        "filename": safe_filename,
        "file_type": (
            "image"
            if extension in image_extensions
            else "video"
        )
    }