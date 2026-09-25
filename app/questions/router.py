from fastapi import APIRouter, HTTPException, Query, status
from app.questions.schema import AdminQuestionListResponse, AdminQuestionResponse, CandidateQuestionListResponse, CandidateQuestionResponse, QuestionCreate, QuestionUpdate
from app.questions import service
from app.core.dependencies import db_dependency, user_dependency, admin_dependency

router = APIRouter()

@router.post("/assessment/{assessment_id}", response_model=AdminQuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question( assessment_id: int, question_data: QuestionCreate, current_admin: admin_dependency, db: db_dependency):
    return service.create_question(db = db, assessment_id = assessment_id, question_data = question_data)

@router.get("/", response_model=CandidateQuestionListResponse)
def get_questions(current_user: user_dependency, db: db_dependency, assessment_id: int | None = None, search: str | None = None, question_type: str | None = None, difficulty: str | None = None, sort_by: str = "created_at", sort_order: str = "desc", page: int = 1, limit: int = 10):
    return service.get_questions(db = db, assessment_id = assessment_id, search = search, question_type = question_type, difficulty = difficulty, sort_by = sort_by, sort_order = sort_order, page = page, limit = limit, published_only = True)

@router.get("/admin", response_model=AdminQuestionListResponse)
def get_admin_questions(current_admin: admin_dependency, db: db_dependency, assessment_id: int | None = None, search: str | None = None, question_type: str | None = None, difficulty: str | None = None, sort_by: str = "created_at", sort_order: str = "desc", page: int = 1, limit: int = 10):
    return service.get_questions(db = db, assessment_id = assessment_id, search = search, question_type = question_type, difficulty = difficulty, sort_by = sort_by, sort_order = sort_order, page = page, limit = limit, published_only = False)

@router.get(
    "/{question_id}",
    response_model=CandidateQuestionResponse
)
def get_question(
    question_id: int,
    current_user: user_dependency,
    db: db_dependency
):

    question = service.get_question(
        db=db,
        question_id=question_id
    )

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    if question.assessment.status != "published":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This question is not available"
        )

    return question


# =====================================================
# UPDATE
# =====================================================

@router.put(
    "/{question_id}",
    response_model=AdminQuestionResponse
)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_admin: admin_dependency,
    db: db_dependency
):

    question = service.update_question(
        db=db,
        question_id=question_id,
        question_data=question_data
    )

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question

@router.delete("/{question_id}")
def delete_question(question_id: int, current_admin: admin_dependency, db: db_dependency):
    deleted = service.delete_question(db=db, question_id=question_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return {"message": "Question deleted successfully"}