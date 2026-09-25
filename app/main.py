from fastapi import FastAPI
import app.database.models as models
from app.database.database import engine, Base
from app.auth.router import router as auth_router
from app.assessments.router import router as assessment_router
from app.questions.router import router as question_router
from app.submissions.router import router as submission_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CodeAssess API", description="Developer Assessment & Coding Platform API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://codeassessaus.netlify.app"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(assessment_router, prefix="/assessments", tags=["Assessments"])
app.include_router(question_router, prefix="/questions", tags=["Questions"])
app.include_router(submission_router, prefix="/submissions", tags=["Submissions"])

@app.get("/")
def root():
    return {"message": "Welcome to CodeAssess API"}