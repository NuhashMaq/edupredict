export type AcademicRecordPublic = {
  id: string;
  student_user_id: string;
  created_at: string;
  updated_at: string;

  attendance_pct: number;
  assignments_pct: number;
  quizzes_pct: number;
  exams_pct: number;
  gpa: number;
  term?: string | null;
};

export type AcademicRecordList = {
  items: AcademicRecordPublic[];
  total: number;
};
