from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    profile_image = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")
    submissions = relationship("Submission", back_populates="user")
    assessments = relationship("Assessment", back_populates="creator")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    passing_marks = Column(Integer, nullable=False)
    status = Column(String, default="draft", nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    creator = relationship("User", back_populates="assessments")
    questions = relationship("Question", back_populates="assessment", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="assessment")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)
    marks = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    assessment = relationship("Assessment", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="question")
    coding_submissions = relationship("CodingSubmission", back_populates="question")

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)

    question = relationship("Question", back_populates="options")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    score = Column(Float, nullable=True)
    status = Column(String, default="started", nullable=False)
    percentage = Column(Float, nullable=True)

    user = relationship("User", back_populates="submissions")
    assessment = relationship("Assessment", back_populates="submissions")
    answers = relationship("Answer", back_populates="submission", cascade="all, delete-orphan")
    coding_submissions = relationship("CodingSubmission", back_populates="submission", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, default=False, nullable=False)
    marks_obtained = Column(Float, default=0, nullable=False)

    submission = relationship("Submission", back_populates="answers")
    question = relationship("Question", back_populates="answers")

class CodingSubmission(Base):
    __tablename__ = "coding_submissions"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String, nullable=False)
    status = Column(String, default="pending", nullable=False)
    test_cases_passed = Column(Integer, default=0, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    submission = relationship("Submission", back_populates="coding_submissions")
    question = relationship("Question", back_populates="coding_submissions")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="password_reset_tokens")