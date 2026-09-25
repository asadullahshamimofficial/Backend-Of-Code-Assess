import math
from sqlalchemy.orm import Session
from app.database.models import Assessment
from app.assessments import repository

def create_assessment(db: Session, title: str, description: str | None, category: str, difficulty: str, duration: int, total_marks: int, passing_marks: int, created_by: int):
    if passing_marks > total_marks:
        raise ValueError("Passing marks cannot be greater than total marks")
    assessment = Assessment(
        title=title, description=description, category=category, difficulty=difficulty,
        duration=duration, total_marks=total_marks, passing_marks=passing_marks, created_by=created_by
    )
    return repository.create_assessment(db, assessment)

def get_assessment(db: Session, assessment_id: int):
    return repository.get_assessment_by_id(db, assessment_id)

def get_assessments(db: Session, search: str | None = None, category: str | None = None, difficulty: str | None = None, status: str | None = None, sort_by: str = "created_at", sort_order: str = "desc", page: int = 1, limit: int = 10, published_only: bool = False):
    skip = (page - 1) * limit
    assessments, total = repository.get_assessments(
        db, search=search, category=category, difficulty=difficulty,
        status=status, sort_by=sort_by, sort_order=sort_order,
        skip=skip, limit=limit, published_only=published_only
    )
    total_pages = math.ceil(total / limit) if total > 0 else 0
    return {
        "items": assessments,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }

def update_assessment(db: Session, assessment: Assessment, data: dict):
    new_total = data.get("total_marks", assessment.total_marks)
    new_passing = data.get("passing_marks", assessment.passing_marks)
    if new_passing > new_total:
        raise ValueError("Passing marks cannot be greater than total marks")
    for key, value in data.items():
        setattr(assessment, key, value)
    return repository.update_assessment(db, assessment)

def delete_assessment(db: Session, assessment: Assessment):
    repository.delete_assessment(db, assessment)