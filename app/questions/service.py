import math
from sqlalchemy.orm import Session
from app.database.models import Question, Option
from app.questions import repository

def create_question(db: Session, assessment_id: int, question_data):
    if hasattr(question_data, "model_dump"):
        data = question_data.model_dump()
    elif isinstance(question_data, dict):
        data = question_data
    else:
        data = {"question_text": question_data.question_text, "question_type": question_data.question_type, "marks": question_data.marks, "difficulty": question_data.difficulty, "options": getattr(question_data, "options", [])}

    q_type = data.get("question_type", "mcq").lower()
    question = Question(
        assessment_id=assessment_id,
        question_text=data["question_text"],
        question_type=q_type,
        marks=data.get("marks", 10),
        difficulty=data.get("difficulty", "Medium")
    )
    db.add(question)
    db.flush()

    for opt in data.get("options", []):
        opt_text = opt.get("option_text") if isinstance(opt, dict) else getattr(opt, "option_text", "")
        is_corr = opt.get("is_correct", False) if isinstance(opt, dict) else getattr(opt, "is_correct", False)
        option = Option(question_id=question.id, option_text=opt_text, is_correct=is_corr)
        repository.create_option(db, option)

    db.commit()
    db.refresh(question)
    return question

def get_question(db: Session, question_id: int):
    return repository.get_question_by_id(db, question_id)

def get_questions(db: Session, assessment_id: int | None = None, search: str | None = None, question_type: str | None = None, difficulty: str | None = None, sort_by: str = "created_at", sort_order: str = "desc", page: int = 1, limit: int = 10, published_only: bool = False):
    skip = (page - 1) * limit
    questions, total = repository.get_questions(
        db, assessment_id=assessment_id, search=search, question_type=question_type, difficulty=difficulty,
        sort_by=sort_by, sort_order=sort_order, skip=skip, limit=limit
    )
    total_pages = math.ceil(total / limit) if total > 0 else 0
    return {
        "items": questions,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }

def update_question(db: Session, question_id: int, question_data):
    question = repository.get_question_by_id(db, question_id)
    if not question:
        return None
    data = question_data.model_dump(exclude_unset=True) if hasattr(question_data, "model_dump") else question_data

    if "options" in data:
        repository.delete_options(db, question.id)
        db.flush()
        for opt in data.pop("options"):
            opt_text = opt.get("option_text") if isinstance(opt, dict) else getattr(opt, "option_text", "")
            is_corr = opt.get("is_correct", False) if isinstance(opt, dict) else getattr(opt, "is_correct", False)
            repository.create_option(db, Option(question_id=question.id, option_text=opt_text, is_correct=is_corr))

    for k, v in data.items():
        setattr(question, k, v)
    return repository.update_question(db, question)

def delete_question(db: Session, question_id: int):
    question = repository.get_question_by_id(db, question_id)
    if not question:
        return False
    repository.delete_question(db, question)
    return True