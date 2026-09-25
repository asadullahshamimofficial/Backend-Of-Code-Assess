from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.models import Answer, CodingSubmission, Submission, Question
from app.submissions import repository

def start_assessment(db: Session, assessment_id: int, user_id: int):
    assessment = repository.get_assessment_by_id(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if assessment.status != "published":
        raise HTTPException(status_code=400, detail="Assessment not available")

    existing = repository.get_active_submission(db, user_id, assessment_id)
    if existing:
        return existing
    submission = Submission(user_id=user_id, assessment_id=assessment_id, status="started")
    return repository.create_submission(db, submission)

def get_submission(db: Session, submission_id: int, user_id: int):
    sub = repository.get_user_submission(db, submission_id, user_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub

def save_answer(db: Session, submission_id: int, user_id: int, question_id: int, answer_text: str):
    sub = get_submission(db, submission_id, user_id)
    if sub.status != "started":
        raise HTTPException(status_code=400, detail="Submission already completed")

    question = db.query(Question).filter(Question.id == question_id, Question.assessment_id == sub.assessment_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    correct_option = next((o for o in question.options if o.is_correct), None)
    is_correct = bool(correct_option and answer_text.strip().lower() == correct_option.option_text.strip().lower())
    marks = float(question.marks) if is_correct else 0.0

    existing = repository.get_answer(db, submission_id, question_id)
    if existing:
        existing.answer = answer_text
        existing.is_correct = is_correct
        existing.marks_obtained = marks
        return repository.update_answer(db, existing)

    new_ans = Answer(submission_id=submission_id, question_id=question_id, answer=answer_text, is_correct=is_correct, marks_obtained=marks)
    return repository.create_answer(db, new_ans)

def save_coding_submission(db: Session, submission_id: int, user_id: int, question_id: int, code: str, language: str):
    sub = get_submission(db, submission_id, user_id)
    if sub.status != "started":
        raise HTTPException(status_code=400, detail="Submission already completed")

    existing = repository.get_coding_submission(db, submission_id, question_id)
    if existing:
        existing.code = code
        existing.language = language
        return repository.update_coding_submission(db, existing)

    coding_sub = CodingSubmission(submission_id=submission_id, question_id=question_id, code=code, language=language, status="pending")
    return repository.create_coding_submission(db, coding_sub)

def submit_assessment(db: Session, submission_id: int, user_id: int):
    sub = get_submission(db, submission_id, user_id)
    if sub.status != "started":
        raise HTTPException(status_code=400, detail="Already submitted")

    assessment = repository.get_assessment_by_id(db, sub.assessment_id)
    answers = repository.get_submission_answers(db, submission_id)
    coding_subs = repository.get_submission_coding_submissions(db, submission_id)

    total_score = sum(a.marks_obtained for a in answers)
    sub.score = total_score
    sub.submitted_at = datetime.now(timezone.utc)

    if coding_subs:
        sub.status = "pending_review"
        sub.percentage = None
    else:
        sub.status = "submitted"
        sub.percentage = (total_score / assessment.total_marks * 100) if assessment and assessment.total_marks else 0

    return repository.update_submission(db, sub)

def get_submission_detail(db: Session, submission_id: int, user_id: int):
    sub = get_submission(db, submission_id, user_id)
    return {
        "submission": sub,
        "answers": repository.get_submission_answers(db, submission_id),
        "coding_submissions": repository.get_submission_coding_submissions(db, submission_id),
    }

def get_result(db: Session, submission_id: int, user_id: int):
    sub = get_submission(db, submission_id, user_id)
    if sub.status == "started":
        raise HTTPException(status_code=400, detail="Assessment not submitted yet")

    assessment = repository.get_assessment_by_id(db, sub.assessment_id)
    total = assessment.total_marks if assessment else 100
    pass_marks = assessment.passing_marks if assessment else 50
    score = sub.score or 0

    return {
        "submission_id": sub.id,
        "assessment_id": sub.assessment_id,
        "score": score,
        "total_marks": total,
        "percentage": sub.percentage,
        "passing_marks": pass_marks,
        "passed": score >= pass_marks,
        "status": sub.status,
    }

def get_my_submissions(db: Session, user_id: int):
    subs = repository.get_user_submissions(db, user_id)
    return {"items": subs, "total": len(subs)}

def get_all_submissions(db: Session):
    return repository.get_all_submissions(db)