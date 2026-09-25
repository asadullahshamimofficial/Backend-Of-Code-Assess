from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.database.models import Question, Option

def create_question(db: Session, question: Question):
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

def get_question_by_id(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()

def get_questions(db: Session, assessment_id: int | None = None, search: str | None = None, question_type: str | None = None, difficulty: str | None = None, sort_by: str = "created_at", sort_order: str = "desc", skip: int = 0, limit: int = 10):
    query = db.query(Question)
    if assessment_id is not None:
        query = query.filter(Question.assessment_id == assessment_id)
    if search:
        query = query.filter(Question.question_text.ilike(f"%{search}%"))
    if question_type:
        query = query.filter(Question.question_type == question_type)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    total = query.count()

    sort_columns = {"id": Question.id, "marks": Question.marks, "difficulty": Question.difficulty, "created_at": Question.created_at}
    sort_column = sort_columns.get(sort_by, Question.created_at)
    query = query.order_by(asc(sort_column) if sort_order.lower() == "asc" else desc(sort_column))

    return query.offset(skip).limit(limit).all(), total

def update_question(db: Session, question: Question):
    db.commit()
    db.refresh(question)
    return question

def delete_question(db: Session, question: Question):
    db.delete(question)
    db.commit()

def delete_options(db: Session, question_id: int):
    db.query(Option).filter(Option.question_id == question_id).delete(synchronize_session=False)

def create_option(db: Session, option: Option):
    db.add(option)
    db.flush()
    return option