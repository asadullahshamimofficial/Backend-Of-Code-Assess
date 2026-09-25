from datetime import datetime, timedelta, timezone
from app.database.database import SessionLocal
from app.database.models import User, Assessment, Question, Option, Submission, Answer, CodingSubmission

def seed():
    db = SessionLocal()
    try:
        # Find admin user or create one
        admin = db.query(User).filter(User.role == "admin").first()
        if not admin:
            admin = db.query(User).first()
        admin_id = admin.id if admin else 1

        # Find candidate users
        candidate = db.query(User).filter(User.email == "asad@gmail.com").first()
        if not candidate:
            candidate = db.query(User).filter(User.role == "user").first()
        candidate_id = candidate.id if candidate else admin_id

        # =========================================================
        # 1. ASSESSMENTS
        # =========================================================
        assessments_data = [
            {
                "title": "React.js & Frontend Architecture",
                "description": "Comprehensive evaluation covering React Hooks, Virtual DOM, Component Lifecycle, and Performance Optimization.",
                "category": "Frontend",
                "difficulty": "Medium",
                "duration": 45,
                "total_marks": 50,
                "passing_marks": 30,
                "status": "published",
                "created_by": admin_id,
                "questions": [
                    {
                        "text": "What is the primary benefit of the Virtual DOM in React?",
                        "type": "mcq",
                        "marks": 10,
                        "difficulty": "Easy",
                        "options": [
                            ("It directly updates the browser DOM synchronously", False),
                            ("It batches updates and minimizes expensive browser reflows", True),
                            ("It eliminates the need for HTML and CSS entirely", False),
                            ("It makes HTTP network requests execute faster", False),
                        ]
                    },
                    {
                        "text": "Which React hook is specifically designed to perform side effects like subscriptions or data fetching?",
                        "type": "mcq",
                        "marks": 10,
                        "difficulty": "Easy",
                        "options": [
                            ("useState", False),
                            ("useMemo", False),
                            ("useEffect", True),
                            ("useCallback", False),
                        ]
                    },
                    {
                        "text": "What is the correct syntax to memoize an expensive calculated value between re-renders?",
                        "type": "mcq",
                        "marks": 10,
                        "difficulty": "Medium",
                        "options": [
                            ("useCallback(() => compute(), [deps])", False),
                            ("useMemo(() => compute(), [deps])", True),
                            ("useRef(compute())", False),
                            ("useEffect(() => compute(), [deps])", False),
                        ]
                    },
                    {
                        "text": "Write a clean function in JavaScript that debounces any callback function with a specified delay in milliseconds.",
                        "type": "coding",
                        "marks": 20,
                        "difficulty": "Medium",
                        "options": []
                    }
                ]
            },
            {
                "title": "Python & Data Structures Mastery",
                "description": "Evaluate core Python mechanics, OOP paradigms, dictionary internals, and algorithmic data manipulation.",
                "category": "Python",
                "difficulty": "Medium",
                "duration": 60,
                "total_marks": 60,
                "passing_marks": 40,
                "status": "published",
                "created_by": admin_id,
                "questions": [
                    {
                        "text": "What is the average time complexity of searching a key in a Python dict?",
                        "type": "mcq",
                        "marks": 10,
                        "difficulty": "Easy",
                        "options": [
                            ("O(n)", False),
                            ("O(log n)", False),
                            ("O(1)", True),
                            ("O(n^2)", False),
                        ]
                    },
                    {
                        "text": "What does the 'yield' keyword do when used inside a Python function?",
                        "type": "mcq",
                        "marks": 10,
                        "difficulty": "Medium",
                        "options": [
                            ("Terminates the program immediately", False),
                            ("Turns the function into a generator iterator", True),
                            ("Imports an external library module", False),
                            ("Deletes local variables from memory", False),
                        ]
                    },
                    {
                        "text": "Implement a Python function `two_sum(nums, target)` that returns the indices of the two numbers that add up to target in O(n) time.",
                        "type": "coding",
                        "marks": 40,
                        "difficulty": "Medium",
                        "options": []
                    }
                ]
            },
            {
                "title": "Backend REST API & Microservices",
                "description": "Assessment testing HTTP semantics, authentication protocols (OAuth2/JWT), database query design, and stateless architecture.",
                "category": "Backend",
                "difficulty": "Hard",
                "duration": 60,
                "total_marks": 80,
                "passing_marks": 50,
                "status": "published",
                "created_by": admin_id,
                "questions": [
                    {
                        "text": "Which of the following HTTP methods is strictly considered IDEMPOTENT by REST standards?",
                        "type": "mcq",
                        "marks": 15,
                        "difficulty": "Medium",
                        "options": [
                            ("POST", False),
                            ("PATCH", False),
                            ("PUT", True),
                            ("CONNECT", False),
                        ]
                    },
                    {
                        "text": "What HTTP status code should a server return when a client request lacks valid authentication credentials?",
                        "type": "mcq",
                        "marks": 15,
                        "difficulty": "Easy",
                        "options": [
                            ("400 Bad Request", False),
                            ("401 Unauthorized", True),
                            ("403 Forbidden", False),
                            ("404 Not Found", False),
                        ]
                    },
                    {
                        "text": "Write a Python FastAPI middleware function that verifies a Bearer JWT token from the Authorization header.",
                        "type": "coding",
                        "marks": 50,
                        "difficulty": "Hard",
                        "options": []
                    }
                ]
            },
            {
                "title": "JavaScript Core & Asynchronous Mechanics",
                "description": "Test understanding of Closures, Prototype chains, Event Loop, Microtasks, and Promise concurrency.",
                "category": "JavaScript",
                "difficulty": "Easy",
                "duration": 30,
                "total_marks": 40,
                "passing_marks": 25,
                "status": "published",
                "created_by": admin_id,
                "questions": [
                    {
                        "text": "What is logged when calling `typeof NaN` in standard JavaScript?",
                        "type": "mcq",
                        "marks": 10,
                        "difficulty": "Easy",
                        "options": [
                            ("'undefined'", False),
                            ("'nan'", False),
                            ("'number'", True),
                            ("'object'", False),
                        ]
                    },
                    {
                        "text": "Which queue takes precedence during event loop execution in JavaScript?",
                        "type": "mcq",
                        "marks": 10,
                        "difficulty": "Medium",
                        "options": [
                            ("Macrotask Queue (setTimeout/setInterval)", False),
                            ("Microtask Queue (Promise.then/queueMicrotask)", True),
                            ("Rendering Queue", False),
                            ("Worker Queue", False),
                        ]
                    },
                    {
                        "text": "Implement a recursive function `deepClone(obj)` in JavaScript that clones nested objects without modifying the original.",
                        "type": "coding",
                        "marks": 20,
                        "difficulty": "Medium",
                        "options": []
                    }
                ]
            },
            {
                "title": "Fullstack Cloud & DevOps Engineering (Draft)",
                "description": "Upcoming test on Docker containerization, CI/CD pipeline triggers, and cloud deployment setups.",
                "category": "Fullstack",
                "difficulty": "Hard",
                "duration": 75,
                "total_marks": 100,
                "passing_marks": 60,
                "status": "draft",
                "created_by": admin_id,
                "questions": [
                    {
                        "text": "In Docker, what is the key difference between CMD and ENTRYPOINT?",
                        "type": "mcq",
                        "marks": 20,
                        "difficulty": "Medium",
                        "options": [
                            ("CMD sets default arguments that can be overridden; ENTRYPOINT sets the executable container process", True),
                            ("CMD runs during build time; ENTRYPOINT runs during container runtime", False),
                            ("They are completely synonymous with no behavioral difference", False),
                            ("ENTRYPOINT only works on Linux images", False),
                        ]
                    }
                ]
            }
        ]

        created_assessments = []
        for a_data in assessments_data:
            # Check if exists by title
            existing = db.query(Assessment).filter(Assessment.title == a_data["title"]).first()
            if existing:
                created_assessments.append(existing)
                continue

            assessment = Assessment(
                title=a_data["title"],
                description=a_data["description"],
                category=a_data["category"],
                difficulty=a_data["difficulty"],
                duration=a_data["duration"],
                total_marks=a_data["total_marks"],
                passing_marks=a_data["passing_marks"],
                status=a_data["status"],
                created_by=a_data["created_by"]
            )
            db.add(assessment)
            db.flush()

            # Add questions
            for q_data in a_data["questions"]:
                question = Question(
                    assessment_id=assessment.id,
                    question_text=q_data["text"],
                    question_type=q_data["type"],
                    marks=q_data["marks"],
                    difficulty=q_data["difficulty"]
                )
                db.add(question)
                db.flush()

                # Add options
                for opt_text, is_corr in q_data["options"]:
                    option = Option(
                        question_id=question.id,
                        option_text=opt_text,
                        is_correct=is_corr
                    )
                    db.add(option)

            db.commit()
            db.refresh(assessment)
            created_assessments.append(assessment)

        print(f"Created/Verified {len(created_assessments)} assessments.")

        # =========================================================
        # 2. DUMMY SUBMISSIONS
        # =========================================================
        react_assessment = created_assessments[0]
        python_assessment = created_assessments[1]

        # Submission 1: Completed & Passed (React test)
        sub1 = db.query(Submission).filter(
            Submission.user_id == candidate_id,
            Submission.assessment_id == react_assessment.id
        ).first()

        now = datetime.now(timezone.utc)

        if not sub1:
            sub1 = Submission(
                user_id=candidate_id,
                assessment_id=react_assessment.id,
                started_at=now - timedelta(days=2, hours=1),
                submitted_at=now - timedelta(days=2, minutes=30),
                score=30.0,
                percentage=60.0,
                status="submitted"
            )
            db.add(sub1)
            db.flush()

            # Add sample answers
            for q in react_assessment.questions:
                if q.question_type == "mcq":
                    corr = next((o for o in q.options if o.is_correct), None)
                    if corr:
                        ans = Answer(
                            submission_id=sub1.id,
                            question_id=q.id,
                            answer=corr.option_text,
                            is_correct=True,
                            marks_obtained=float(q.marks)
                        )
                        db.add(ans)

            db.commit()
            print(f"Added completed submission #{sub1.id} for user {candidate_id}")

        # Submission 2: Python test pending review with coding submission
        sub2 = db.query(Submission).filter(
            Submission.user_id == candidate_id,
            Submission.assessment_id == python_assessment.id
        ).first()

        if not sub2:
            sub2 = Submission(
                user_id=candidate_id,
                assessment_id=python_assessment.id,
                started_at=now - timedelta(hours=3),
                submitted_at=now - timedelta(hours=2),
                score=20.0,
                percentage=None,
                status="pending_review"
            )
            db.add(sub2)
            db.flush()

            for q in python_assessment.questions:
                if q.question_type == "mcq":
                    corr = next((o for o in q.options if o.is_correct), None)
                    ans = Answer(
                        submission_id=sub2.id,
                        question_id=q.id,
                        answer=corr.option_text if corr else "O(1)",
                        is_correct=True,
                        marks_obtained=float(q.marks)
                    )
                    db.add(ans)
                elif q.question_type == "coding":
                    coding_sub = CodingSubmission(
                        submission_id=sub2.id,
                        question_id=q.id,
                        code="""def two_sum(nums, target):
    lookup = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in lookup:
            return [lookup[diff], i]
        lookup[num] = i
    return []""",
                        language="python",
                        status="pending",
                        test_cases_passed=2
                    )
                    db.add(coding_sub)

            db.commit()
            print(f"Added pending review submission #{sub2.id} for user {candidate_id}")

        print("Seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
