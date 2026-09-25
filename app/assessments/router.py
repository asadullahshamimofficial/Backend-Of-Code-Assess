from fastapi import APIRouter, HTTPException, Query, status
from app.assessments.schema import AssessmentCreate, AssessmentUpdate, AssessmentResponse, AssessmentListResponse
from app.assessments import service
from app.core.dependencies import db_dependency, user_dependency, admin_dependency

router = APIRouter()

@router.post("/", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
def create(data: AssessmentCreate, db: db_dependency, current_admin: admin_dependency):
    try:
        return service.create_assessment(
            db, data.title, data.description, data.category, data.difficulty,
            data.duration, data.total_marks, data.passing_marks, current_admin.id
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/", response_model=AssessmentListResponse)
def get_all(
    db: db_dependency,
    current_user: user_dependency,
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    is_admin = current_user.role == "admin"
    return service.get_assessments(
        db, search=search, category=category, difficulty=difficulty,
        status=status_filter if is_admin else None, sort_by=sort_by, sort_order=sort_order,
        page=page, limit=limit, published_only=not is_admin
    )

@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_one(assessment_id: int, db: db_dependency, current_user: user_dependency):
    assessment = service.get_assessment(db, assessment_id)
    if not assessment or (current_user.role != "admin" and assessment.status != "published"):
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@router.put("/{assessment_id}", response_model=AssessmentResponse)
def update(assessment_id: int, data: AssessmentUpdate, db: db_dependency, current_admin: admin_dependency):
    assessment = service.get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    try:
        return service.update_assessment(db, assessment, data.model_dump(exclude_unset=True))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(assessment_id: int, db: db_dependency, current_admin: admin_dependency):
    assessment = service.get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    service.delete_assessment(db, assessment)
    return None