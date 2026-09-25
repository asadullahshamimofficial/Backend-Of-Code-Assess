from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session
from app.database.models import Assessment

def create_assessment(db: Session, assessment: Assessment):
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment

def get_assessment_by_id(db: Session, assessment_id: int):
    return db.query(Assessment).filter(Assessment.id == assessment_id).first()

def get_assessments(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    difficulty: str | None = None,
    status: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 10,
    published_only: bool = False
):
    query = db.query(Assessment)

    if published_only:
        query = query.filter(Assessment.status == "published")

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(or_( Assessment.title.ilike(search_pattern), Assessment.description.ilike(search_pattern), Assessment.category.ilike(search_pattern)))

    if category:
        query = query.filter(Assessment.category == category)

    if difficulty:
        query = query.filter(Assessment.difficulty == difficulty)

    if status and not published_only:
        query = query.filter(Assessment.status == status)

    total = query.count()
    sort_columns = {
        "id": Assessment.id,
        "title": Assessment.title,
        "duration": Assessment.duration,
        "total_marks": Assessment.total_marks,
        "passing_marks": Assessment.passing_marks,
        "created_at": Assessment.created_at,
        "updated_at": Assessment.updated_at
    }
    sort_column = sort_columns.get(sort_by, Assessment.created_at)

    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    assessments = query.offset(skip).limit(limit).all()
    return assessments, total

def update_assessment(db: Session, assessment: Assessment):
    db.commit()
    db.refresh(assessment)
    return assessment

def delete_assessment(db: Session, assessment: Assessment):
    db.delete(assessment)
    db.commit()