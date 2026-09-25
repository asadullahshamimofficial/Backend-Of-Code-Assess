from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class OptionCreate(BaseModel):
    option_text: str = Field(min_length=1, max_length=500)
    is_correct: bool = False


class AdminOptionResponse(BaseModel):
    id: int
    question_id: int
    option_text: str
    is_correct: bool
    model_config = {"from_attributes": True}


class CandidateOptionResponse(BaseModel):
    id: int
    question_id: int
    option_text: str
    model_config = {"from_attributes": True}


class QuestionCreate(BaseModel):
    question_text: str = Field(min_length=3)
    question_type: str = Field(min_length=2, max_length=50)
    marks: int = Field(gt=0)
    difficulty: str = Field(min_length=2, max_length=50)
    options: list[OptionCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_question(self):
        qtype = self.question_type.lower()
        if qtype not in {"mcq", "coding"}:
            raise ValueError("question_type must be either 'mcq' or 'coding'")
        if qtype == "mcq":
            if len(self.options) < 2:
                raise ValueError("MCQ must have at least 2 options")
            correct = [o for o in self.options if o.is_correct]
            if len(correct) != 1:
                raise ValueError("MCQ must have exactly one correct option")
        if qtype == "coding" and self.options:
            raise ValueError("Coding question cannot have options")
        return self


class QuestionUpdate(BaseModel):
    question_text: str | None = Field(default=None, min_length=3)
    question_type: str | None = Field(default=None, min_length=2, max_length=50)
    marks: int | None = Field(default=None, gt=0)
    difficulty: str | None = Field(default=None, min_length=2, max_length=50)
    options: list[OptionCreate] | None = None


class AdminQuestionResponse(BaseModel):
    id: int
    assessment_id: int
    question_text: str
    question_type: str
    marks: int
    difficulty: str
    created_at: datetime
    options: list[AdminOptionResponse] = Field(default_factory=list)
    model_config = {"from_attributes": True}


class CandidateQuestionResponse(BaseModel):
    id: int
    assessment_id: int
    question_text: str
    question_type: str
    marks: int
    difficulty: str
    created_at: datetime
    options: list[CandidateOptionResponse] = Field(default_factory=list)
    model_config = {"from_attributes": True}


class AdminQuestionListResponse(BaseModel):
    items: list[AdminQuestionResponse]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool


class CandidateQuestionListResponse(BaseModel):
    items: list[CandidateQuestionResponse]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool