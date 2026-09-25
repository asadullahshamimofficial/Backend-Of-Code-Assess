from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.database import engine
import app.database.models as models
from app.auth.router import router as auth_router
from app.assessments.router import router as assessment_router
from app.questions.router import router as question_router
from app.submissions.router import router as submission_router
from app.users.router import router as user_router

app = FastAPI(title="CodeAssess API")

origins = [o.strip() for o in settings.FRONTEND_ORIGIN.split(",") if o.strip()]
for o in ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"]:
    if o not in origins:
        origins.append(o)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(assessment_router, prefix="/assessments", tags=["Assessments"])
app.include_router(question_router, prefix="/questions", tags=["Questions"])
app.include_router(submission_router, prefix="/submissions", tags=["Submissions"])
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to CodeAssess API"}

@app.get("/health")
def health():
    return {"status": "ok"}
