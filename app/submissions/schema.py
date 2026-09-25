from datetime import datetime
from pydantic import BaseModel, Field

# =========================
# START SUBMISSION
# =========================

class SubmissionStartResponse(BaseModel):
    id: int
    user_id: int
    assessment_id: int
    started_at: datetime
    status: str
    model_config = {"from_attributes": True}

# =========================
# ANSWER
# =========================

class AnswerCreate(BaseModel):
    question_id: int
    answer: str = Field(min_length=1)

class AnswerResponse(BaseModel):
    id: int
    submission_id: int
    question_id: int
    answer: str | None = None
    is_correct: bool
    marks_obtained: float
    model_config = {"from_attributes": True}

# =========================
# CODING SUBMISSION
# =========================

class CodingSubmissionCreate(BaseModel):
    question_id: int
    code: str = Field(min_length=1)
    language: str = Field(min_length=1, max_length=50)

class CodingSubmissionResponse(BaseModel):
    id: int
    submission_id: int
    question_id: int
    code: str
    language: str
    status: str
    test_cases_passed: int
    submitted_at: datetime
    model_config = {"from_attributes": True}

# =========================
# SUBMISSION RESPONSE
# =========================

class SubmissionAssessmentBrief(BaseModel):
    id: int
    title: str
    category: str | None = None
    total_marks: int | None = None
    model_config = {"from_attributes": True}

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    assessment_id: int
    started_at: datetime
    submitted_at: datetime | None = None
    score: float | None = None
    status: str
    percentage: float | None = None
    assessment: SubmissionAssessmentBrief | None = None
    model_config = {"from_attributes": True}

# =========================
# SUBMISSION DETAIL
# =========================

class SubmissionDetailResponse(BaseModel):
    submission: SubmissionResponse
    answers: list[AnswerResponse]
    coding_submissions: list[CodingSubmissionResponse]

# =========================
# RESULT
# =========================

class SubmissionResultResponse(BaseModel):
    submission_id: int
    assessment_id: int
    score: float
    total_marks: int
    percentage: float | None = None
    passing_marks: int
    passed: bool
    status: str

# =========================
# MY SUBMISSIONS
# =========================

class MySubmissionListResponse(BaseModel):
    items: list[SubmissionResponse]
    total: int

class AdminSubmissionResponse(BaseModel):
    id: int
    user_id: int
    assessment_id: int
    started_at: datetime
    submitted_at: datetime | None = None
    score: float | None = None
    status: str
    percentage: float | None = None
    assessment: SubmissionAssessmentBrief | None = None
    model_config = {"from_attributes": True}

class AdminSubmissionListResponse(BaseModel):
    items: list[AdminSubmissionResponse]
    total: int