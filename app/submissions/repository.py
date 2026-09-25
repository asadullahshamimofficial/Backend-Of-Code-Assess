from sqlalchemy.orm import Session
from app.database.models import Answer, Assessment, CodingSubmission, Submission


def get_assessment_by_id(db: Session, assessment_id: int):
    return db.query(Assessment).filter(Assessment.id == assessment_id).first()


def create_submission(db: Session, submission: Submission):
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def get_submission_by_id(db: Session, submission_id: int):
    return db.query(Submission).filter(Submission.id == submission_id).first()


def get_user_submission(db: Session, submission_id: int, user_id: int):
    return db.query(Submission).filter(Submission.id == submission_id, Submission.user_id == user_id).first()


def get_user_submissions(db: Session, user_id: int):
    return db.query(Submission).filter(Submission.user_id == user_id).order_by(Submission.started_at.desc()).all()


def get_active_submission(db: Session, user_id: int, assessment_id: int):
    return db.query(Submission).filter(
        Submission.user_id == user_id,
        Submission.assessment_id == assessment_id,
        Submission.status == "started"
    ).first()


def update_submission(db: Session, submission: Submission):
    db.commit()
    db.refresh(submission)
    return submission


def get_answer(db: Session, submission_id: int, question_id: int):
    return db.query(Answer).filter(
        Answer.submission_id == submission_id,
        Answer.question_id == question_id
    ).first()


def create_answer(db: Session, answer: Answer):
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def update_answer(db: Session, answer: Answer):
    db.commit()
    db.refresh(answer)
    return answer


def get_submission_answers(db: Session, submission_id: int):
    return db.query(Answer).filter(Answer.submission_id == submission_id).all()


def get_coding_submission(db: Session, submission_id: int, question_id: int):
    return db.query(CodingSubmission).filter(
        CodingSubmission.submission_id == submission_id,
        CodingSubmission.question_id == question_id
    ).first()


def create_coding_submission(db: Session, coding_submission: CodingSubmission):
    db.add(coding_submission)
    db.commit()
    db.refresh(coding_submission)
    return coding_submission


def update_coding_submission(db: Session, coding_submission: CodingSubmission):
    db.commit()
    db.refresh(coding_submission)
    return coding_submission


def get_submission_coding_submissions(db: Session, submission_id: int):
    return db.query(CodingSubmission).filter(CodingSubmission.submission_id == submission_id).all()


def get_all_submissions(db: Session):
    return db.query(Submission).order_by(Submission.started_at.desc()).all()