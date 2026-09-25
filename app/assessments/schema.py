from datetime import datetime
from pydantic import BaseModel, Field

class AssessmentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    category: str = Field(min_length=2, max_length=100)
    difficulty: str = Field(min_length=2, max_length=50)
    duration: int = Field(gt=0)
    total_marks: int = Field(gt=0)
    passing_marks: int = Field(gt=0)

class AssessmentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    category: str | None = Field(default=None, min_length=2, max_length=100)
    difficulty: str | None = Field(default=None, min_length=2, max_length=50)
    duration: int | None = Field(default=None, gt=0)
    total_marks: int | None = Field(default=None, gt=0)
    passing_marks: int | None = Field(default=None, gt=0)
    status: str | None = None

class AssessmentResponse(BaseModel):
    id: int
    title: str
    description: str | None
    category: str
    difficulty: str
    duration: int
    total_marks: int
    passing_marks: int
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
    
class AssessmentListResponse(BaseModel):
    items: list[AssessmentResponse]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool