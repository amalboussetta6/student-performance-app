from pydantic import BaseModel


class StudentData(BaseModel):
    gender: str
    study_hours_per_week: float
    attendance_rate: float
    past_exam_scores: float
    parental_education_level: str
    internet_access_at_home: str
    extracurricular_activities: str


class ChatData(BaseModel):
    question: str

    predicted_score: float
    result: str

    recommendations: list

    student: StudentData