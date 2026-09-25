from fastapi import APIRouter
from app.core.dependencies import user_dependency, db_dependency, admin_dependency
from app.submissions.schema import (
    AnswerCreate, AnswerResponse, CodingSubmissionCreate, CodingSubmissionResponse,
    MySubmissionListResponse, SubmissionDetailResponse, SubmissionResponse,
    SubmissionResultResponse, SubmissionStartResponse, AdminSubmissionListResponse
)
from app.submissions import service

router = APIRouter()

@router.post("/start/{assessment_id}", response_model=SubmissionStartResponse)
def start_assessment(assessment_id: int, current_user: user_dependency, db: db_dependency):
    return service.start_assessment(db, assessment_id, current_user.id)

@router.get("/my", response_model=MySubmissionListResponse)
def get_my_submissions(current_user: user_dependency, db: db_dependency):
    return service.get_my_submissions(db, current_user.id)

@router.get("/admin/all", response_model=AdminSubmissionListResponse)
def get_all_submissions(current_admin: admin_dependency, db: db_dependency):
    submissions = service.get_all_submissions(db)
    return {"items": submissions, "total": len(submissions)}

@router.get("/{submission_id}", response_model=SubmissionDetailResponse)
def get_submission(submission_id: int, current_user: user_dependency, db: db_dependency):
    return service.get_submission_detail(db, submission_id, current_user.id)

@router.post("/{submission_id}/answers", response_model=AnswerResponse)
def save_answer(submission_id: int, answer_data: AnswerCreate, current_user: user_dependency, db: db_dependency):
    return service.save_answer(db, submission_id, current_user.id, answer_data.question_id, answer_data.answer)

@router.post("/{submission_id}/coding", response_model=CodingSubmissionResponse)
def save_coding_submission(submission_id: int, coding_data: CodingSubmissionCreate, current_user: user_dependency, db: db_dependency):
    return service.save_coding_submission(db, submission_id, current_user.id, coding_data.question_id, coding_data.code, coding_data.language)

@router.post("/{submission_id}/submit", response_model=SubmissionResponse)
def submit_assessment(submission_id: int, current_user: user_dependency, db: db_dependency):
    return service.submit_assessment(db, submission_id, current_user.id)

@router.get("/{submission_id}/result", response_model=SubmissionResultResponse)
def get_result(submission_id: int, current_user: user_dependency, db: db_dependency):
    return service.get_result(db, submission_id, current_user.id)