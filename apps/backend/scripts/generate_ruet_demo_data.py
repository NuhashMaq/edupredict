from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# Reproducible demo data
SEED = 20260105

# RUET CSE: 4 years x 2 terms
TERM_LABELS = ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1", "4-2"]
# Generate first 6 terms; keep last 2 for future plan/prediction.
TERMS_TO_GENERATE = 6


@dataclass(frozen=True)
class Course:
    semester: int
    code: str
    title: str
    kind: str  # theory|lab
    credits: float


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def grade_from_total_80(total: float) -> tuple[str, float]:
    """Convert total marks out of 80 -> (letter, grade_point out of 4.0)."""
    # Scale-aware bands (roughly mirrors common BD universities, tuned for /80)
    if total >= 72:
        return "A+", 4.00
    if total >= 68:
        return "A", 3.75
    if total >= 64:
        return "A-", 3.50
    if total >= 60:
        return "B+", 3.25
    if total >= 56:
        return "B", 3.00
    if total >= 52:
        return "B-", 2.75
    if total >= 48:
        return "C+", 2.50
    if total >= 44:
        return "C", 2.25
    if total >= 40:
        return "D", 2.00
    return "F", 0.00


def build_courses() -> list[Course]:
    """RUET CSE demo structure: first 6 terms.

    Semester/term labels:
    - 1-1, 1-2, 2-1, 2-2, 3-1, 3-2, 4-1, 4-2

    Course code format requested:
    - Course code is the term prefix (11, 12, 21, ...) + 01-09
    - odd => theory (e.g., 1101, 1103, ... 1109)
    - even => sessional/lab (e.g., 1102, 1104, 1106, 1108)
    """
    courses: list[Course] = []

    # Simple, synthetic course catalog (not official RUET curriculum)
    for sem_idx in range(1, TERMS_TO_GENERATE + 1):
        term_label = TERM_LABELS[sem_idx - 1]  # e.g., 1-1
        term_prefix = term_label.replace("-", "")  # e.g., 11

        # 5 theory courses: 01,03,05,07,09
        for i in range(1, 6):
            n = 2 * i - 1
            code = f"{term_prefix}{n:02d}"
            title = f"Theory Course {term_label} ({n:02d})"
            courses.append(Course(semester=sem_idx, code=code, title=title, kind="theory", credits=3.0))

        # 3 or 4 sessional/labs: 02,04,06,(08)
        lab_count = 3 if sem_idx <= 4 else 4
        for i in range(1, lab_count + 1):
            n = 2 * i
            code = f"{term_prefix}{n:02d}"
            title = f"Sessional/Lab {term_label} ({n:02d})"
            courses.append(Course(semester=sem_idx, code=code, title=title, kind="lab", credits=1.5))

    return courses


def generate_students(n: int) -> list[dict[str, str]]:
    first_names = [
        "Mashfiq",
        "Nafis",
        "Arafat",
        "Sadia",
        "Nusrat",
        "Tanvir",
        "Farhan",
        "Rafi",
        "Ayesha",
        "Mehedi",
        "Zarin",
        "Sakib",
        "Tamim",
        "Raisa",
        "Imran",
        "Tanjila",
        "Hasan",
        "Nabila",
        "Sabbir",
        "Nayeem",
    ]
    last_names = [
        "Hossain",
        "Rahman",
        "Islam",
        "Chowdhury",
        "Sarker",
        "Khan",
        "Ahmed",
        "Nashad",
        "Mahmud",
        "Das",
        "Jahan",
        "Khatun",
        "Roy",
        "Miah",
        "Haque",
    ]

    out: list[dict[str, str]] = []
    base_roll = 2103001
    for i in range(0, n):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        roll = str(base_roll + i)
        email = f"{roll}@student.ruet.ac.bd"
        full_name = f"{fn} {ln}"
        # min length 12 (backend constraint). Keep it simple for demo.
        password = f"Student{roll}Pass!"
        out.append(
            {
                "student_roll": roll,
                "email": email,
                "full_name": full_name,
                "password": password,
                "university": "RUET",
                "department": "CSE",
                "program": "BSc in Engineering",
            }
        )
    return out


def weighted_mean(pairs: Iterable[tuple[float, float]]) -> float:
    num = 0.0
    den = 0.0
    for value, weight in pairs:
        num += value * weight
        den += weight
    return num / den if den else 0.0


def main() -> None:
    random.seed(SEED)

    root = Path(__file__).resolve().parents[1]
    out_dir = root / "data" / "demo_ruet_cse"
    out_dir.mkdir(parents=True, exist_ok=True)

    students = generate_students(60)
    courses = build_courses()

    # --- outputs ---
    students_csv = out_dir / "students_ruet_cse_50.csv"
    course_marks_csv = out_dir / "course_marks_ruet_cse_50x8.csv"
    import_csv = out_dir / "edupredict_academic_import_ruet_cse_50x8.csv"
    predictions_csv = out_dir / "predictions_ruet_cse_50x8.csv"

    # 1) Students (for creating accounts)
    with students_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "student_roll",
                "email",
                "full_name",
                "password",
                "university",
                "department",
                "program",
            ],
        )
        w.writeheader()
        w.writerows(students)

    # 2) Per-course marks and grades
    course_rows: list[dict[str, str]] = []

    # Track CGPA cumulatively by student
    # cumulative: sum(gp*credits), sum(credits)
    cumulative: dict[str, tuple[float, float]] = {s["email"]: (0.0, 0.0) for s in students}

    # For import rows (per student per semester)
    import_rows: list[dict[str, str]] = []
    pred_rows: list[dict[str, str]] = []

    for s in students:
        email = s["email"]
        # Keep a mild personal baseline so each student feels consistent
        base_att = random.uniform(6.0, 9.5)  # out of 10
        base_asg = random.uniform(5.5, 9.5)  # out of 10
        base_final = random.uniform(30.0, 52.0)  # out of 60

        prev_cgpa = 0.0

        for sem_idx in range(1, TERMS_TO_GENERATE + 1):
            term_label = TERM_LABELS[sem_idx - 1]
            sem_courses = [c for c in courses if c.semester == sem_idx]

            # semester drift: students improve or dip slightly
            drift = random.uniform(-0.6, 0.8)

            sem_att_scores: list[float] = []
            sem_asg_scores: list[float] = []
            sem_quiz_scores: list[float] = []
            sem_exam_scores: list[float] = []

            sem_pairs: list[tuple[float, float]] = []

            for c in sem_courses:
                # Labs typically have higher attendance/assignments, slightly lower final variance.
                kind_boost = 0.45 if c.kind == "lab" else 0.0

                attendance_10 = clamp(random.gauss(base_att + kind_boost + drift * 0.15, 1.1), 0.0, 10.0)
                assignments_10 = clamp(random.gauss(base_asg + kind_boost + drift * 0.10, 1.2), 0.0, 10.0)
                # Quizzes weren't in your marks list, but EduPredict import expects it.
                # We'll generate it as a sibling to assignments (also out of 10).
                quizzes_10 = clamp(random.gauss((assignments_10 + base_asg) / 2.0, 1.3), 0.0, 10.0)

                final_60 = clamp(random.gauss(base_final + drift * 1.4, 7.5), 0.0, 60.0)

                total_80 = attendance_10 + assignments_10 + final_60
                letter, gp = grade_from_total_80(total_80)

                course_rows.append(
                    {
                        "student_email": email,
                        "student_roll": s["student_roll"],
                        "university": s["university"],
                        "department": s["department"],
                        "semester": term_label,
                        "course_code": c.code,
                        "course_title": c.title,
                        "course_type": c.kind,
                        "credits": f"{c.credits:.1f}",
                        "attendance_10": f"{attendance_10:.1f}",
                        "assignments_10": f"{assignments_10:.1f}",
                        "final_60": f"{final_60:.1f}",
                        "total_80": f"{total_80:.1f}",
                        "letter_grade": letter,
                        "grade_point_4": f"{gp:.2f}",
                    }
                )

                sem_pairs.append((gp, c.credits))
                sem_att_scores.append(attendance_10)
                sem_asg_scores.append(assignments_10)
                sem_quiz_scores.append(quizzes_10)
                sem_exam_scores.append(final_60)

                # update cumulative for CGPA
                sum_gp_x_cr, sum_cr = cumulative[email]
                cumulative[email] = (sum_gp_x_cr + gp * c.credits, sum_cr + c.credits)

            sem_gpa = weighted_mean(sem_pairs)
            cum_gp_x_cr, cum_cr = cumulative[email]
            cgpa = (cum_gp_x_cr / cum_cr) if cum_cr else 0.0

            # These are used by the app's CSV import (expects percentages)
            attendance_pct = int(round(clamp(sum(sem_att_scores) / len(sem_att_scores), 0.0, 10.0) * 10.0))
            assignments_pct = int(round(clamp(sum(sem_asg_scores) / len(sem_asg_scores), 0.0, 10.0) * 10.0))
            quizzes_pct = int(round(clamp(sum(sem_quiz_scores) / len(sem_quiz_scores), 0.0, 10.0) * 10.0))
            exams_pct = int(round(clamp((sum(sem_exam_scores) / len(sem_exam_scores)) / 60.0, 0.0, 1.0) * 100.0))

            # Use CGPA in the import column named `gpa` (UI label is now CGPA).
            import_rows.append(
                {
                    "student_email": email,
                    "attendance_pct": str(attendance_pct),
                    "assignments_pct": str(assignments_pct),
                    "quizzes_pct": str(quizzes_pct),
                    "exams_pct": str(exams_pct),
                    "gpa": f"{cgpa:.2f}",
                    "term": term_label,
                }
            )

            # Simple demo prediction (illustrative only)
            # Higher CGPA + better attendance -> lower risk.
            # Add a small trend effect: improving CGPA reduces risk.
            slope = cgpa - prev_cgpa
            risk = sigmoid(
                (2.35 - cgpa) * 1.25
                + (0.78 - (attendance_pct / 100.0)) * 1.10
                + (0.70 - (exams_pct / 100.0)) * 0.90
                + (-slope) * 0.85
            )
            risk = float(clamp(risk, 0.0, 1.0))
            if risk >= 0.66:
                level = "High"
            elif risk >= 0.33:
                level = "Medium"
            else:
                level = "Low"

            predicted_next_cgpa = clamp(cgpa + slope * 0.6 + random.uniform(-0.12, 0.12), 0.0, 4.0)

            pred_rows.append(
                {
                    "student_email": email,
                    "term": term_label,
                    "cgpa": f"{cgpa:.2f}",
                    "semester_gpa": f"{sem_gpa:.2f}",
                    "risk_probability": f"{risk:.3f}",
                    "risk_level": level,
                    "predicted_next_cgpa": f"{predicted_next_cgpa:.2f}",
                }
            )

            prev_cgpa = cgpa

    with course_marks_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "student_email",
                "student_roll",
                "university",
                "department",
                "semester",
                "course_code",
                "course_title",
                "course_type",
                "credits",
                "attendance_10",
                "assignments_10",
                "final_60",
                "total_80",
                "letter_grade",
                "grade_point_4",
            ],
        )
        w.writeheader()
        w.writerows(course_rows)

    with import_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "student_email",
                "attendance_pct",
                "assignments_pct",
                "quizzes_pct",
                "exams_pct",
                "gpa",
                "term",
            ],
        )
        w.writeheader()
        w.writerows(import_rows)

    with predictions_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "student_email",
                "term",
                "cgpa",
                "semester_gpa",
                "risk_probability",
                "risk_level",
                "predicted_next_cgpa",
            ],
        )
        w.writeheader()
        w.writerows(pred_rows)

    print("Generated demo RUET CSE dataset:")
    print(f"- {students_csv}")
    print(f"- {course_marks_csv}")
    print(f"- {import_csv}")
    print(f"- {predictions_csv}")


if __name__ == "__main__":
    main()
